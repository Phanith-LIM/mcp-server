# Simple FastMCP Server

A minimal, modular server and client implementation using FastMCP for rapid prototyping and testing of Model Context Protocol (MCP) workflows. This project demonstrates how to set up a FastMCP server with Server-Sent Events (SSE) transport, interact with SQLite databases, and extend functionality with custom tools. It is designed for easy deployment, quick experimentation.

## Installation
Install UV package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
or pipx
```bash
pip install uv
```

## Install Dependencies
```bash
uv sync
```

## Usage
Run the server:
```bash
fastmcp run main.py --transport streamable-http --host 0.0.0.0 --port 8080
```
Run the client:
```bash
uv run client.py
```

## Project Structure

```
├── main.py           # FastMCP server entry point
├── client.py         # Example client script
├── Dockerfile        # Containerization support
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # uv dependency lock file
├── resource/
│   ├── chinook.db    # Example SQLite database
│   └── titanic.db    # Example SQLite database
├── tools/
│   ├── __init__.py
│   └── sql_server.py # SQL tool for server
├── utils/
│   └── __init__.py
└── README.md         # Project documentation
```

## Features
- FastMCP server with Server-Sent Events (SSE) transport
- Example client for testing
- SQLite database resources for demo/testing
- Modular tools for SQL operations
- Docker support for easy deployment

## Configuration
- Edit `main.py` to customize server logic or database connections.
- Place additional SQLite databases in the `resource/` directory as needed.

## Troubleshooting
- Ensure all dependencies are installed with `uv sync`.
- If you encounter issues with `fastmcp`, check that it is installed and available in your PATH.
- For database errors, verify the presence and integrity of files in `resource/`.
