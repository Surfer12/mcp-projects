# Dockerfile

# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy server code into container
COPY tools_server.py /app/tools_server.py

# Install required Python MCP libraries
RUN pip install "mcp[cli]"

# Expose MCP server via stdio
CMD ["python", "/app/tools_server.py"]