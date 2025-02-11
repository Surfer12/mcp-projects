"""
Web-focused tool for handling HTTP requests, API interactions, and web scraping capabilities.
"""
import os
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import time
import datetime

class WebTool:
    def __init__(self):
        """Initialize the WebTool with default configuration."""
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AnalyticsBot/1.0)",
            "Accept": "text/html,application/json,application/xhtml+xml",
        }
        self.timeout = 30

    def make_request(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the specified URL.

        Args:
            url: Target URL for the request
            method: HTTP method (GET, POST, etc.)
            params: URL parameters
            data: Request body data
            headers: Custom headers
            timeout: Request timeout in seconds

        Returns:
            Dictionary containing response data and metadata
        """
        try:
            merged_headers = {**self.headers, **(headers or {})}
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                json=data if method.upper() != "GET" else None,
                headers=merged_headers,
                timeout=timeout or self.timeout,
            )

            content_type = response.headers.get("content-type", "")

            result = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "success": response.ok,
            }

            if "application/json" in content_type:
                result["data"] = response.json()
            else:
                result["text"] = response.text

            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": None,
            }

    def scrape_webpage(
        self,
        url: str,
        selectors: Optional[List[str]] = None,
        extract_links: bool = False,
    ) -> Dict[str, Any]:
        """
        Scrape content from a webpage using BeautifulSoup.

        Args:
            url: Target URL to scrape
            selectors: List of CSS selectors to extract specific content
            extract_links: Whether to extract all links from the page

        Returns:
            Dictionary containing scraped content and metadata
        """
        try:
            response = self.make_request(url)
            if not response["success"]:
                return response

            soup = BeautifulSoup(response.get("text", ""), "html.parser")
            result = {
                "success": True,
                "title": soup.title.string if soup.title else None,
                "content": {},
            }

            if selectors:
                for selector in selectors:
                    elements = soup.select(selector)
                    result["content"][selector] = [elem.get_text(strip=True) for elem in elements]

            if extract_links:
                result["links"] = [
                    {
                        "text": a.get_text(strip=True),
                        "href": a.get("href"),
                    }
                    for a in soup.find_all("a", href=True)
                ]

            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def analyze_api_response(
        self,
        response_data: Dict[str, Any],
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze an API response for structure and validity.

        Args:
            response_data: The API response data to analyze
            schema: Optional JSON schema to validate against

        Returns:
            Dictionary containing analysis results
        """
        try:
            analysis = {
                "success": True,
                "data_type": type(response_data).__name__,
                "structure": {},
            }

            def analyze_structure(data: Any, path: str = "") -> None:
                if isinstance(data, dict):
                    analysis["structure"][path] = "object"
                    for key, value in data.items():
                        new_path = f"{path}.{key}" if path else key
                        analyze_structure(value, new_path)
                elif isinstance(data, list):
                    analysis["structure"][path] = f"array[{len(data)}]"
                    if data:
                        analyze_structure(data[0], f"{path}[0]")
                else:
                    analysis["structure"][path] = type(data).__name__

            analyze_structure(response_data)

            if schema:
                # Basic schema validation
                def validate_schema(data: Any, schema_part: Dict[str, Any]) -> List[str]:
                    errors = []
                    schema_type = schema_part.get("type")

                    if schema_type == "object":
                        if not isinstance(data, dict):
                            errors.append(f"Expected object, got {type(data).__name__}")
                        else:
                            properties = schema_part.get("properties", {})
                            for prop, prop_schema in properties.items():
                                if prop in data:
                                    errors.extend(validate_schema(data[prop], prop_schema))
                    elif schema_type == "array":
                        if not isinstance(data, list):
                            errors.append(f"Expected array, got {type(data).__name__}")

                    return errors

                validation_errors = validate_schema(response_data, schema)
                analysis["schema_valid"] = not bool(validation_errors)
                if validation_errors:
                    analysis["schema_errors"] = validation_errors

            return analysis
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def monitor_endpoint(
        self,
        url: str,
        interval: int = 60,
        max_attempts: int = 5,
    ) -> Dict[str, Any]:
        """
        Monitor an endpoint for availability and response times.

        Args:
            url: The endpoint URL to monitor
            interval: Time between checks in seconds
            max_attempts: Maximum number of monitoring attempts

        Returns:
            Dictionary containing monitoring results
        """
        results = []
        try:
            for _ in range(max_attempts):
                start_time = time.time()
                response = self.make_request(url)
                end_time = time.time()

                result = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "response_time": end_time - start_time,
                    "status_code": response.get("status_code"),
                    "success": response.get("success", False),
                }
                results.append(result)

                if _ < max_attempts - 1:  # Don't sleep after the last attempt
                    time.sleep(interval)

            return {
                "success": True,
                "url": url,
                "results": results,
                "summary": {
                    "total_checks": len(results),
                    "successful_checks": sum(1 for r in results if r["success"]),
                    "average_response_time": sum(r["response_time"] for r in results) / len(results),
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "partial_results": results,
            }