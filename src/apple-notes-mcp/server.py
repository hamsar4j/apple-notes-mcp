import logging
from mcp.server.fastmcp import FastMCP
from notes_client import NotesClient
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("apple-notes")
notes_ops = NotesClient()


@mcp.tool()
def create_note(title: str, content: str, folder: Optional[str] = None) -> str:
    """
    Create a new note in Apple Notes.

    Args:
        title: The title/name of the note
        content: The content/body of the note
        folder: Optional folder name to create the note in

    Returns:
        Success message or error description
    """
    try:
        result = notes_ops.create_note(title, content, folder)
        if result.success:
            return f"Note '{title}' created successfully"
        else:
            return f"Failed to create note: {result.error}"
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        return f"Error creating note: {str(e)}"


@mcp.tool()
def list_notes(folder: Optional[str] = None) -> str:
    """
    List all notes or notes in a specific folder.

    Args:
        folder: Optional folder name to filter notes by

    Returns:
        List of note names or error message
    """
    try:
        notes = notes_ops.list_notes(folder)
        if notes:
            notes_list = "\n".join(f"• {note}" for note in notes)
            folder_text = f" in folder '{folder}'" if folder else ""
            return f"Notes{folder_text}:\n{notes_list}"
        else:
            folder_text = f" in folder '{folder}'" if folder else ""
            return f"No notes found{folder_text}"
    except Exception as e:
        logger.error(f"Error listing notes: {e}")
        return f"Error listing notes: {str(e)}"


@mcp.tool()
def get_note_content(note_name: str) -> str:
    """
    Get the content of a specific note.

    Args:
        note_name: The name of the note to retrieve

    Returns:
        Note content or error message
    """
    try:
        note = notes_ops.get_note_content(note_name)
        if note:
            folder_info = f" (in folder: {note.folder})" if note.folder else ""
            return f"Note: {note.name}{folder_info}\n\n{note.body}"
        else:
            return f"Note '{note_name}' not found"
    except Exception as e:
        logger.error(f"Error getting note content: {e}")
        return f"Error getting note content: {str(e)}"


@mcp.tool()
def update_note_content(note_name: str, new_content: str) -> str:
    """
    Update the content of an existing note.

    Args:
        note_name: The name of the note to update
        new_content: The new content for the note

    Returns:
        Success message or error description
    """
    try:
        result = notes_ops.update_note_content(note_name, new_content)
        if result.success:
            return f"Note '{note_name}' content updated successfully"
        else:
            return f"Failed to update note: {result.error}"
    except Exception as e:
        logger.error(f"Error updating note content: {e}")
        return f"Error updating note content: {str(e)}"


@mcp.tool()
def update_note_title(old_name: str, new_name: str) -> str:
    """
    Update the title of an existing note.

    Args:
        old_name: The current name of the note
        new_name: The new name for the note

    Returns:
        Success message or error description
    """
    try:
        result = notes_ops.update_note_title(old_name, new_name)
        if result.success:
            return f"Note title updated from '{old_name}' to '{new_name}'"
        else:
            return f"Failed to update note title: {result.error}"
    except Exception as e:
        logger.error(f"Error updating note title: {e}")
        return f"Error updating note title: {str(e)}"


@mcp.tool()
def create_folder(folder_name: str) -> str:
    """
    Create a new folder in Apple Notes.

    Args:
        folder_name: The name of the folder to create

    Returns:
        Success message or error description
    """
    try:
        result = notes_ops.create_folder(folder_name)
        if result.success:
            return f"Folder '{folder_name}' created successfully"
        else:
            return f"Failed to create folder: {result.error}"
    except Exception as e:
        logger.error(f"Error creating folder: {e}")
        return f"Error creating folder: {str(e)}"


@mcp.tool()
def list_folders() -> str:
    """
    List all folders in Apple Notes.

    Returns:
        List of folder names or error message
    """
    try:
        folders = notes_ops.list_folders()
        if folders:
            folders_list = "\n".join(f"{folder}" for folder in folders)
            return f"Folders in Apple Notes:\n{folders_list}"
        else:
            return "No folders found"
    except Exception as e:
        logger.error(f"Error listing folders: {e}")
        return f"Error listing folders: {str(e)}"


@mcp.tool()
def move_note_to_folder(note_name: str, folder_name: str) -> str:
    """
    Move a note to a different folder.

    Args:
        note_name: The name of the note to move
        folder_name: The name of the target folder

    Returns:
        Success message or error description
    """
    try:
        result = notes_ops.move_note_to_folder(note_name, folder_name)
        if result.success:
            return f"Note '{note_name}' moved to folder '{folder_name}'"
        else:
            return f"Failed to move note: {result.error}"
    except Exception as e:
        logger.error(f"Error moving note: {e}")
        return f"Error moving note: {str(e)}"


@mcp.tool()
def search_notes(search_term: str) -> str:
    """
    Search for notes containing a specific term.

    Args:
        search_term: The term to search for in note titles and content

    Returns:
        List of matching note names or error message
    """
    try:
        matching_notes = notes_ops.search_notes(search_term)
        if matching_notes:
            notes_list = "\n".join(f"{note}" for note in matching_notes)
            return f"Notes containing '{search_term}':\n{notes_list}"
        else:
            return f"No notes found containing '{search_term}'"
    except Exception as e:
        logger.error(f"Error searching notes: {e}")
        return f"Error searching notes: {str(e)}"


@mcp.tool()
def get_folder_info(folder_name: str) -> str:
    """
    Get information about a specific folder.

    Args:
        folder_name: The name of the folder

    Returns:
        Folder information or error message
    """
    try:
        folder_info = notes_ops.get_folder_info(folder_name)
        if folder_info:
            note_count = (
                folder_info.note_count
                if folder_info.note_count is not None
                else "unknown"
            )
            return f"Folder: {folder_info.name}\nNotes: {note_count}"
        else:
            return f"Folder '{folder_name}' not found"
    except Exception as e:
        logger.error(f"Error getting folder info: {e}")
        return f"Error getting folder info: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
