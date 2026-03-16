# Obsidian MCP

Un servidor MCP (Model Context Protocol) que permite a modelos de lenguaje como Claude interactuar directamente con tu vault de Obsidian a través de la [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api).

## Requisitos previos

- [Obsidian](https://obsidian.md/) instalado con el plugin **Local REST API** activo
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes recomendado)

## Instalación

```bash
git clone https://github.com/tu-usuario/obsidian-mcp.git
cd obsidian-mcp
uv sync
```

## Configuración

Crea un fichero `.env` en la raíz del proyecto con la API key de Obsidian Local REST API:

```env
OBSIDIAN_KEY=tu_api_key_aqui
```

La API key se obtiene desde Obsidian: **Settings → Local REST API → API Key**.

## Herramientas disponibles

| Herramienta | Descripción |
|---|---|
| `new file` | Crea un nuevo archivo `.md` en el vault |
| `read file` | Lee el contenido de un archivo `.md` |
| `append data to file` | Añade contenido al final de un archivo existente |
| `update data to file` | Reemplaza texto dentro de un archivo |
| `delete file` | Elimina un archivo del vault |
| `new folder` | Crea una carpeta en el vault |
| `read folder` | Lista el contenido de una carpeta |

> Todos los archivos deben tener extensión `.md`. Las rutas pueden ser relativas a la raíz del vault.

## Uso con Claude Code

Añade el servidor al fichero de configuración MCP de Claude Code (`claude_desktop_config.json` o `~/.claude/mcp_servers.json`):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/ruta/a/obsidian-mcp"
    }
  }
}
```

## Arquitectura

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

El servidor se comunica con el LLM mediante el protocolo MCP sobre `stdio`, y reenvía las operaciones a la API REST local de Obsidian (HTTPS en `127.0.0.1:27124`).

## Dependencias

- [`mcp`](https://github.com/anthropics/mcp) — framework FastMCP para construir servidores MCP
- [`httpx`](https://www.python-httpx.org/) — cliente HTTP para comunicarse con la API de Obsidian
- [`pydantic`](https://docs.pydantic.dev/) — validación de parámetros de las herramientas
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) — carga de variables de entorno
