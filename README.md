# Apple Notes MCP Server

A Model Context Protocol (MCP) server that provides CRU(D) tools for Apple Notes using AppleScript integration. This server allows you to create, read, and update notes and folders in the Apple Notes app on your MacOS devices.

## Features

### Note Tools

- **Create notes** - Add new notes with title and content
- **List notes** - Get all notes or notes in a specific folder
- **Get note content** - Retrieve the full content of a specific note
- **Update note content** - Modify the body of existing notes
- **Update note title** - Rename existing notes
- **Search notes** - Find notes by content or title

### Folder Tools

- **Create folders** - Add new folders to organize notes
- **List folders** - Get all available folders
- **Get folder info** - Get folder details including note count
- **Move notes** - Move notes between folders

## Installation

1. **Clone the repository:**

  ```bash
  git clone <repository-url>
  cd apple-notes-mcp
  ```

2. **Install dependencies:**

  ```bash
  uv venv
  uv sync
  ```

## Usage

### Available Tools

#### Note Management

- `create_note(title, content, folder=None)` - Create a new note
- `list_notes(folder=None)` - List all notes or notes in a folder
- `get_note_content(note_name)` - Get the content of a specific note
- `update_note_content(note_name, new_content)` - Update note content
- `update_note_title(old_name, new_name)` - Rename a note
- `search_notes(search_term)` - Search for notes containing a term

#### Folder Management

- `create_folder(folder_name)` - Create a new folder
- `list_folders()` - List all folders
- `get_folder_info(folder_name)` - Get folder information
- `move_note_to_folder(note_name, folder_name)` - Move a note to a folder

## Configuration

### MCP Client Configuration

To use this server with an MCP client (like Claude Desktop), add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "apple-notes": {
      "command": "uv",
      "args": [
        "--directory",
        "apple-notes-mcp/src/apple-notes-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```
