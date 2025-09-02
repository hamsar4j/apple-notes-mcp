import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
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
def get_folder_info(folder_name: str) -> dict:
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
    title: str, content: str, folder_name: Optional[str] = None
) -> TextContent:
    """Create a new note in Apple Notes.

    Args:
        title: The title/name of the note
        content: The content/body of the note
        folder_name: Optional folder name to create the note in

    Returns:
        Result message as TextContent
    """
    result = notes_client.create_note(title, content, folder_name)
    message = (
        f"Note '{title}' created successfully"
        if result.success
        else f"Failed to create note: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def list_notes(folder_name: Optional[str] = None) -> TextContent:
    """List all notes or notes in a specific folder.

    Args:
        folder_name: Optional folder name to filter notes by

    Returns:
        List of note names as TextContent
    """
    notes = notes_client.list_notes(folder_name)
    folder_text = f" in folder '{folder_name}'" if folder_name else ""
    if notes:
        message = f"Found {len(notes)} notes{folder_text}:\n" + "\n".join(notes)
    else:
        message = f"No notes found{folder_text}"
    return TextContent(type="text", text=message)


@mcp.tool()
def read_note(note_name: str) -> TextContent:
    """Read the content of a specific note.

    Args:
        note_name: The name of the note to read

    Returns:
        Note content as TextContent

    Raises:
        ValueError: If the note is not found
    """
    note = notes_client.get_note_content(note_name)
    if not note:
        raise ValueError(f"Note '{note_name}' not found")

    # Format the note content in a readable way
    content_parts = [f"# {note.name}"]
    if note.folder:
        content_parts.append(f"Folder: {note.folder}")
    if note.creation_date:
        content_parts.append(f"Created: {note.creation_date}")
    if note.modification_date:
        content_parts.append(f"Modified: {note.modification_date}")
    content_parts.append("")
    content_parts.append(note.body)

    formatted_content = "\n".join(content_parts)
    return TextContent(type="text", text=formatted_content)


@mcp.tool()
def update_note_content(note_name: str, new_content: str) -> TextContent:
    """Update the content of an existing note.

    Args:
        note_name: The name of the note to update
        new_content: The new content for the note

    Returns:
        Result message as TextContent
    """
    result = notes_client.update_note_content(note_name, new_content)
    message = (
        f"Note '{note_name}' content updated successfully"
        if result.success
        else f"Failed to update note: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def update_note_title(old_name: str, new_name: str) -> TextContent:
    """Update the title of an existing note.

    Args:
        old_name: The current name of the note
        new_name: The new name for the note

    Returns:
        Result message as TextContent
    """
    result = notes_client.update_note_title(old_name, new_name)
    message = (
        f"Note title updated from '{old_name}' to '{new_name}'"
        if result.success
        else f"Failed to update note title: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def delete_note(note_name: str) -> TextContent:
    """Delete a note from Apple Notes.

    Args:
        note_name: The name of the note to delete

    Returns:
        Result message as TextContent
    """
    result = notes_client.delete_note(note_name)
    message = (
        f"Note '{note_name}' deleted successfully"
        if result.success
        else f"Failed to delete note: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def search_notes(search_term: str) -> TextContent:
    """Search for notes containing a specific term.

    Args:
        search_term: The term to search for in note titles and content

    Returns:
        List of matching note names as TextContent
    """
    matching_notes = notes_client.search_notes(search_term)
    if matching_notes:
        message = (
            f"Found {len(matching_notes)} notes containing '{search_term}':\n"
            + "\n".join(matching_notes)
        )
    else:
        message = f"No notes found containing '{search_term}'"
    return TextContent(type="text", text=message)


@mcp.tool()
def create_folder(folder_name: str) -> TextContent:
    """Create a new folder in Apple Notes.

    Args:
        folder_name: The name of the folder to create

    Returns:
        Result message as TextContent
    """
    result = notes_client.create_folder(folder_name)
    message = (
        f"Folder '{folder_name}' created successfully"
        if result.success
        else f"Failed to create folder: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def list_folders() -> TextContent:
    """List all folders in Apple Notes.

    Returns:
        List of folder names as TextContent
    """
    folders = notes_client.list_folders()
    if folders:
        message = f"Found {len(folders)} folders:\n" + "\n".join(folders)
    else:
        message = "No folders found"
    return TextContent(type="text", text=message)


@mcp.tool()
def move_note_to_folder(note_name: str, folder_name: str) -> TextContent:
    """Move a note to a different folder.

    Args:
        note_name: The name of the note to move
        folder_name: The name of the target folder

    Returns:
        Result message as TextContent
    """
    result = notes_client.move_note_to_folder(note_name, folder_name)
    message = (
        f"Note '{note_name}' moved to folder '{folder_name}'"
        if result.success
        else f"Failed to move note: {result.error}"
    )
    return TextContent(type="text", text=message)


@mcp.tool()
def delete_folder(folder_name: str) -> TextContent:
    """Delete a folder from Apple Notes.

    Args:
        folder_name: The name of the folder to delete

    Returns:
        Result message as TextContent
    """
    result = notes_client.delete_folder(folder_name)
    message = (
        f"Folder '{folder_name}' deleted successfully"
        if result.success
        else f"Failed to delete folder: {result.error}"
    )
    return TextContent(type="text", text=message)


def main() -> None:
    """Entry point for the apple-notes-mcp command."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
