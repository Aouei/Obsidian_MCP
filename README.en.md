# Obsidian MCP

An MCP (Model Context Protocol) server that lets language models like Claude interact directly with your Obsidian vault via the [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api).

## Prerequisites

- [Obsidian](https://obsidian.md/) with the **Local REST API** plugin enabled
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended package manager)

## Installation

```bash
git clone https://github.com/your-username/obsidian-mcp.git
cd obsidian-mcp
uv sync
```

## Configuration

Create a `.env` file at the project root with your Obsidian Local REST API key:

```env
OBSIDIAN_KEY=your_api_key_here
```

The API key is found in Obsidian under **Settings → Local REST API → API Key**.

## Available tools

| Tool | Description |
|---|---|
| `new file` | Creates a new `.md` file in the vault |
| `read file` | Reads the content of a `.md` file |
| `append data to file` | Appends content to the bottom of an existing file |
| `update data to file` | Replaces text within a file |
| `delete file` | Deletes a file from the vault |
| `new folder` | Creates a folder in the vault |
| `read folder` | Lists the contents of a folder |

> All files must have the `.md` extension. Paths can be relative to the vault root.

## Usage with Claude Code

Add the server to your Claude Code MCP config file (`claude_desktop_config.json` or `~/.claude/mcp_servers.json`):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/obsidian-mcp"
    }
  }
}
```

## Architecture

```
Claude / LLM
     │
     │ MCP (stdio)
     ▼
  server.py  ──── httpx ────▶  Obsidian Local REST API (https://127.0.0.1:27124)
                                        │
                                        ▼
                                  Obsidian Vault
```

The server communicates with the LLM over MCP via `stdio`, forwarding operations to Obsidian's local REST API (HTTPS on `127.0.0.1:27124`).

## Dependencies

- [`mcp`](https://github.com/anthropics/mcp) — FastMCP framework for building MCP servers
- [`httpx`](https://www.python-httpx.org/) — HTTP client for communicating with the Obsidian API
- [`pydantic`](https://docs.pydantic.dev/) — tool parameter validation
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) — environment variable loading
