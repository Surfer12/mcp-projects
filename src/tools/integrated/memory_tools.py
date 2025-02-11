"""
Memory tools for MCP providing data persistence and retrieval capabilities.
"""

import json
from pathlib import Path
from typing import Any, Optional, Set
import sqlite3
from datetime import datetime

from anthropic.types.beta import BetaToolUnionParam

from ..base import BaseCognitiveTool, CognitiveToolResult


class MemoryTool(BaseCognitiveTool):
    """Tool for memory operations including data persistence and retrieval."""

    name = "memory_tool"
    description = "Executes memory operations for data persistence and retrieval."

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize the memory tool.

        Args:
            storage_dir: Directory for storing persistent data. Defaults to ~/.mcp/memory
        """
        self.storage_dir = storage_dir or Path.home() / '.mcp' / 'memory'
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_dir / 'memory.db'
        self._init_db()

    def __call__(self, **kwargs) -> CognitiveToolResult:
        """Execute a memory operation.

        Args:
            operation: The operation to perform ('store', 'retrieve', 'list', 'delete')
            key: Key for the data
            data: Data to store (for 'store' operation)
            tags: List of tags for the data (for 'store' operation)
            tag_filter: List of tags to filter by (for 'list' operation)
        """
        if not self.validate_args(**kwargs):
            return CognitiveToolResult(
                success=False,
                error="Invalid arguments provided"
            )

        operation = kwargs.get('operation')
        try:
            if operation == 'store':
                result = self._store_data(
                    kwargs['key'],
                    kwargs['data'],
                    kwargs.get('tags', [])
                )
            elif operation == 'retrieve':
                result = self._retrieve_data(kwargs['key'])
            elif operation == 'list':
                result = self._list_data(kwargs.get('tag_filter', []))
            elif operation == 'delete':
                result = self._delete_data(kwargs['key'])
            else:
                return CognitiveToolResult(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )

            return CognitiveToolResult(
                success=True,
                data=result
            )
        except Exception as e:
            return CognitiveToolResult(
                success=False,
                error=str(e)
            )

    def to_anthropic_param(self) -> BetaToolUnionParam:
        """Convert to Anthropic tool parameter format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["store", "retrieve", "list", "delete"],
                            "description": "Operation to perform"
                        },
                        "key": {
                            "type": "string",
                            "description": "Key for the data"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data to store"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tags for the data"
                        },
                        "tag_filter": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Tags to filter by"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }

    def validate_args(self, **kwargs) -> bool:
        """Validate the arguments for this tool."""
        if 'operation' not in kwargs:
            return False

        operation = kwargs['operation']
        if operation == 'store' and ('key' not in kwargs or 'data' not in kwargs):
            return False
        elif operation in ('retrieve', 'delete') and 'key' not in kwargs:
            return False

        return True

    def _init_db(self):
        """Initialize the SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    key TEXT PRIMARY KEY,
                    data TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    key TEXT,
                    tag TEXT,
                    FOREIGN KEY(key) REFERENCES memory(key) ON DELETE CASCADE,
                    PRIMARY KEY(key, tag)
                )
            """)
            conn.commit()

    def _store_data(self, key: str, data: Any, tags: list[str]) -> dict[str, Any]:
        """Store data with tags."""
        now = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            # Store or update the data
            conn.execute("""
                INSERT INTO memory (key, data, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    data = excluded.data,
                    updated_at = excluded.updated_at
            """, (key, json.dumps(data), now, now))

            # Update tags
            conn.execute("DELETE FROM tags WHERE key = ?", (key,))
            conn.executemany(
                "INSERT INTO tags (key, tag) VALUES (?, ?)",
                [(key, tag) for tag in set(tags)]
            )
            conn.commit()

        return {
            'key': key,
            'tags': tags,
            'timestamp': now
        }

    def _retrieve_data(self, key: str) -> dict[str, Any]:
        """Retrieve data and its tags."""
        with sqlite3.connect(self.db_path) as conn:
            # Get the data
            row = conn.execute(
                "SELECT data, created_at, updated_at FROM memory WHERE key = ?",
                (key,)
            ).fetchone()

            if not row:
                return None

            # Get the tags
            tags = [
                tag[0] for tag in conn.execute(
                    "SELECT tag FROM tags WHERE key = ?",
                    (key,)
                ).fetchall()
            ]

            return {
                'key': key,
                'data': json.loads(row[0]),
                'created_at': row[1],
                'updated_at': row[2],
                'tags': tags
            }

    def _list_data(self, tag_filter: list[str]) -> list[dict[str, Any]]:
        """List all data entries, optionally filtered by tags."""
        with sqlite3.connect(self.db_path) as conn:
            if tag_filter:
                # Get keys that have all the specified tags
                keys = conn.execute("""
                    SELECT key
                    FROM tags
                    WHERE tag IN ({})
                    GROUP BY key
                    HAVING COUNT(DISTINCT tag) = ?
                """.format(','.join('?' * len(tag_filter))),
                    (*tag_filter, len(tag_filter))
                ).fetchall()
                keys = [k[0] for k in keys]

                if not keys:
                    return []

                # Get data for these keys
                query = """
                    SELECT m.key, m.data, m.created_at, m.updated_at
                    FROM memory m
                    WHERE m.key IN ({})
                """.format(','.join('?' * len(keys)))
                params = keys
            else:
                query = "SELECT key, data, created_at, updated_at FROM memory"
                params = []

            entries = []
            for row in conn.execute(query, params).fetchall():
                # Get tags for each entry
                tags = [
                    tag[0] for tag in conn.execute(
                        "SELECT tag FROM tags WHERE key = ?",
                        (row[0],)
                    ).fetchall()
                ]

                entries.append({
                    'key': row[0],
                    'data': json.loads(row[1]),
                    'created_at': row[2],
                    'updated_at': row[3],
                    'tags': tags
                })

            return entries

    def _delete_data(self, key: str) -> dict[str, Any]:
        """Delete data and its tags."""
        with sqlite3.connect(self.db_path) as conn:
            # Check if the key exists
            row = conn.execute(
                "SELECT 1 FROM memory WHERE key = ?",
                (key,)
            ).fetchone()

            if not row:
                return {'deleted': False, 'key': key}

            # Delete the data (tags will be cascade deleted)
            conn.execute("DELETE FROM memory WHERE key = ?", (key,))
            conn.commit()

            return {'deleted': True, 'key': key}