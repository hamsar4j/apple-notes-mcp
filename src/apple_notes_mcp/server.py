import logging
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from .notes_client import NotesClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server and Notes client
mcp = FastMCP("apple-notes")
notes_client = NotesClient()


# =============================================================================
# Resources (Read-only access)
# =============================================================================


@mcp.resource("notes:///folder/{folder_name}")
def get_folder_info(folder_name: str) -> Dict[str, Any]:
    """Get information about a specific folder.

    Args:
        folder_name: The name of the folder

    Returns:
        Folder information as structured data

    Raises:
        ValueError: If the folder is not found
    """
    folder_info = notes_client.get_folder_info(folder_name)
    if not folder_info:
        raise ValueError(f"Folder '{folder_name}' not found")

    return {"name": folder_info.name, "note_count": folder_info.note_count}


# =============================================================================
# Tools
# =============================================================================


@mcp.tool()
def create_note(
    title: str, content: str, folder: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new note in Apple Notes.

    Args:
        title: The title/name of the note
        content: The content/body of the note
        folder: Optional folder name to create the note in

    Returns:
        Result with success status and message
    """
    result = notes_client.create_note(title, content, folder)
    return {
        "success": result.success,
        "message": (
            f"Note '{title}' created successfully"
            if result.success
            else f"Failed to create note: {result.error}"
        ),
    }


@mcp.tool()
def list_notes(folder: Optional[str] = None) -> Dict[str, Any]:
    """List all notes or notes in a specific folder.

    Args:
        folder: Optional folder name to filter notes by

    Returns:
        List of note names
    """
    notes = notes_client.list_notes(folder)
    folder_text = f" in folder '{folder}'" if folder else ""
    return {
        "notes": notes,
        "message": (
            f"Found {len(notes)} notes{folder_text}"
            if notes
            else f"No notes found{folder_text}"
        ),
    }


@mcp.tool()
def read_note(note_name: str) -> Dict[str, Any]:
    """Read the content of a specific note.

    Args:
        note_name: The name of the note to read

    Returns:
        Note content as structured data

    Raises:
        ValueError: If the note is not found
    """
    note = notes_client.get_note_content(note_name)
    if not note:
        raise ValueError(f"Note '{note_name}' not found")

    return {
        "name": note.name,
        "body": note.body,
        "folder": note.folder,
        "creation_date": note.creation_date,
        "modification_date": note.modification_date,
    }


@mcp.tool()
def update_note_content(note_name: str, new_content: str) -> Dict[str, Any]:
    """Update the content of an existing note.

    Args:
        note_name: The name of the note to update
        new_content: The new content for the note

    Returns:
        Result with success status and message
    """
    result = notes_client.update_note_content(note_name, new_content)
    return {
        "success": result.success,
        "message": (
            f"Note '{note_name}' content updated successfully"
            if result.success
            else f"Failed to update note: {result.error}"
        ),
    }


@mcp.tool()
def update_note_title(old_name: str, new_name: str) -> Dict[str, Any]:
    """Update the title of an existing note.

    Args:
        old_name: The current name of the note
        new_name: The new name for the note

    Returns:
        Result with success status and message
    """
    result = notes_client.update_note_title(old_name, new_name)
    return {
        "success": result.success,
        "message": (
            f"Note title updated from '{old_name}' to '{new_name}'"
            if result.success
            else f"Failed to update note title: {result.error}"
        ),
    }


@mcp.tool()
def delete_note(note_name: str) -> Dict[str, Any]:
    """Delete a note from Apple Notes.

    Args:
        note_name: The name of the note to delete

    Returns:
        Result with success status and message
    """
    result = notes_client.delete_note(note_name)
    return {
        "success": result.success,
        "message": (
            f"Note '{note_name}' deleted successfully"
            if result.success
            else f"Failed to delete note: {result.error}"
        ),
    }


@mcp.tool()
def search_notes(search_term: str) -> Dict[str, Any]:
    """Search for notes containing a specific term.

    Args:
        search_term: The term to search for in note titles and content

    Returns:
        List of matching note names
    """
    matching_notes = notes_client.search_notes(search_term)
    return {
        "notes": matching_notes,
        "message": (
            f"Found {len(matching_notes)} notes containing '{search_term}'"
            if matching_notes
            else f"No notes found containing '{search_term}'"
        ),
    }


@mcp.tool()
def create_folder(folder_name: str) -> Dict[str, Any]:
    """Create a new folder in Apple Notes.

    Args:
        folder_name: The name of the folder to create

    Returns:
        Result with success status and message
    """
    result = notes_client.create_folder(folder_name)
    return {
        "success": result.success,
        "message": (
            f"Folder '{folder_name}' created successfully"
            if result.success
            else f"Failed to create folder: {result.error}"
        ),
    }


@mcp.tool()
def list_folders() -> Dict[str, Any]:
    """List all folders in Apple Notes.

    Returns:
        List of folder names
    """
    folders = notes_client.list_folders()
    return {
        "folders": folders,
        "message": f"Found {len(folders)} folders" if folders else "No folders found",
    }


@mcp.tool()
def move_note_to_folder(note_name: str, folder_name: str) -> Dict[str, Any]:
    """Move a note to a different folder.

    Args:
        note_name: The name of the note to move
        folder_name: The name of the target folder

    Returns:
        Result with success status and message
    """
    result = notes_client.move_note_to_folder(note_name, folder_name)
    return {
        "success": result.success,
        "message": (
            f"Note '{note_name}' moved to folder '{folder_name}'"
            if result.success
            else f"Failed to move note: {result.error}"
        ),
    }


@mcp.tool()
def delete_folder(folder_name: str) -> Dict[str, Any]:
    """Delete a folder from Apple Notes.

    Args:
        folder_name: The name of the folder to delete

    Returns:
        Result with success status and message
    """
    result = notes_client.delete_folder(folder_name)
    return {
        "success": result.success,
        "message": (
            f"Folder '{folder_name}' deleted successfully"
            if result.success
            else f"Failed to delete folder: {result.error}"
        ),
    }


def main() -> None:
    """Entry point for the apple-notes-mcp command."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
