import httpx
import os


from pathlib import Path
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pydantic import Field


load_dotenv(Path(__file__).parent / ".env")
API_KEY = os.environ.get('OBSIDIAN_KEY')
BASE_URL = 'https://127.0.0.1:27124'
AUTH = {"Authorization": f"Bearer {API_KEY}"}


mcp = FastMCP("Obsidian MCP", log_level="ERROR")

KO = 'KO'


@mcp.tool(
    name="new file",
    description="Creates a new file"
)
def new_file(
    filename: str = Field(description="The filename of the file to create (Can be a relative path)"),
    content: str = Field(description="The content of the file"),
):
    
    headers = {}
    headers["Content-Type"] = "text/markdown; charset=utf-8"
    headers.update(AUTH)

    if not filename.endswith('.md'):
        raise ValueError('The filename must be a markdown file ending with .md')

    httpx.post(
        url=f'{BASE_URL}/vault/{filename}',
        headers=headers,
        content=content,
        verify=False
    )

@mcp.tool(
    name="append data to file",
    description="Append new content at the bottom of the file"
)
def append_data_to_file(
    filename: str = Field(description="The filename of the file to append content (Can be a relative path)"),
    content: str = Field(description="The content to be append"),
):
    headers = {}
    headers["Content-Type"] = "text/markdown; charset=utf-8"
    headers.update(AUTH)

    if not filename.endswith('.md'):
        raise ValueError('The filename must be a markdown file ending with .md')

    response = httpx.post(
        url=f'{BASE_URL}/vault/{filename}',
        headers=headers,
        data=content,
        verify=False
    )

    if response.status_code == 204:
        return 'OK'
    else:
        return response.content

@mcp.tool(
    name="update data to file",
    description="Update new content of the file by replacing existing content"
)
def update_file(
    filename: str = Field(description="The filename of the file to append content (Can be a relative path)"),
    old_content: str = Field(description="The old content to be replaced by new content"),
    new_content: str = Field(description="The new content"),
):
    headers = {}
    headers["Content-Type"] = "text/markdown; charset=utf-8"
    headers.update(AUTH)

    if not filename.endswith('.md'):
        raise ValueError('The filename must be a markdown file ending with .md')

    response = read_file(filename)

    if response == KO:
        return response

    content = response.replace(old_content, new_content)
    response = httpx.put(
        url=f'{BASE_URL}/vault/{filename}',
        headers=headers,
        data=content,
        verify=False
    )

    if response.status_code == 204:
        return 'OK'
    else:
        return response.content

@mcp.tool(
    name="read file",
    description="Reads a file"
)
def read_file(
    filename: str = Field(description="The filename path to read (Can be a relative path)")
):
    if not filename.endswith('.md'):
        raise ValueError('The filename must be a markdown file ending with .md')
    
    response = httpx.get(
        url=f'{BASE_URL}/vault/{filename}',
        headers=AUTH,
        verify=False
    )

    if response.status_code == 404:
        return KO
    
    return response.text

@mcp.tool(
    name="delete file",
    description="Deletes a file"
)
def delete_file(
    filename: str = Field(description="The filename path to delete (Can be a relative path and must have an ending slash '/')")
):
    
    if not filename.endswith('.md'):
        raise ValueError('The filename must be a markdown file ending with .md')
    
    response = httpx.delete(
        url=f'{BASE_URL}/vault/{filename}',
        headers=AUTH,
        verify=False
    )

    if response.status_code == 204:
        return 'OK'
    else:
        return KO
    

@mcp.tool(
    name="new folder",
    description="Creates a folder"
)
def new_folder(
    folder: str = Field(description="The folder path to create (Can be a relative path)")
):
    response = httpx.put(
        url=f'{BASE_URL}/vault/{folder}/.keep',
        headers=AUTH,
        verify=False
    )
    
    if response.status_code in [200, 204]:
        return 'OK'
    else:
        return KO
    
@mcp.tool(
    name="read folder",
    description="Reads a folder"
)
def read_folder(
    folder: str = Field(description="The folder path to read (Can be a relative path and must have an ending slash '/')")
):
    response = httpx.get(
        url=f'{BASE_URL}/vault/{folder}',
        headers=AUTH,
        verify=False
    )

    if response.status_code == 404:
        return 'Not Found'
    
    return response.json()



if __name__ == "__main__":
    mcp.run(transport="stdio")