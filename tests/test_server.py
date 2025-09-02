import pytest
from unittest.mock import patch
from src.apple_notes_mcp.server import (
    read_note,
    get_folder_info,
    create_note,
    list_notes,
    update_note_content,
    update_note_title,
    create_folder,
    list_folders,
    move_note_to_folder,
    search_notes,
    delete_note,
    delete_folder,
)
from src.apple_notes_mcp.models import Note, Folder, AppleScriptResult


@pytest.fixture
def mock_notes_client():
    """Create a mock NotesClient for testing."""
    with patch("src.apple_notes_mcp.server.notes_client") as mock:
        yield mock


def test_read_note_success(mock_notes_client):
    """Test successful retrieval of note content."""
    # Setup mock
    mock_note = Note(name="Test Note", body="This is a test note", folder="Test Folder")
    mock_notes_client.get_note_content.return_value = mock_note

    # Execute
    result = read_note("Test Note")

    # Verify
    assert result["name"] == "Test Note"
    assert result["body"] == "This is a test note"
    assert result["folder"] == "Test Folder"
    mock_notes_client.get_note_content.assert_called_once_with("Test Note")


def test_read_note_no_folder(mock_notes_client):
    """Test retrieving note content when note is not in a folder."""
    # Setup mock
    mock_note = Note(name="Test Note", body="This is a test note", folder=None)
    mock_notes_client.get_note_content.return_value = mock_note

    # Execute
    result = read_note("Test Note")

    # Verify
    assert result["name"] == "Test Note"
    assert result["body"] == "This is a test note"
    assert result["folder"] is None


def test_read_note_not_found(mock_notes_client):
    """Test retrieving content of non-existent note."""
    # Setup mock
    mock_notes_client.get_note_content.return_value = None

    # Execute and verify
    with pytest.raises(ValueError, match="Note 'Non-existent Note' not found"):
        read_note("Non-existent Note")


def test_get_folder_info_success(mock_notes_client):
    """Test successful retrieval of folder info."""
    # Setup mock
    mock_folder = Folder(name="Test Folder", note_count=5)
    mock_notes_client.get_folder_info.return_value = mock_folder

    # Execute
    result = get_folder_info("Test Folder")

    # Verify
    assert result["name"] == "Test Folder"
    assert result["note_count"] == 5
    mock_notes_client.get_folder_info.assert_called_once_with("Test Folder")


def test_get_folder_info_unknown_count(mock_notes_client):
    """Test retrieving folder info when note count is unknown."""
    # Setup mock
    mock_folder = Folder(name="Test Folder", note_count=None)
    mock_notes_client.get_folder_info.return_value = mock_folder

    # Execute
    result = get_folder_info("Test Folder")

    # Verify
    assert result["name"] == "Test Folder"
    assert result["note_count"] is None


def test_get_folder_info_not_found(mock_notes_client):
    """Test retrieving info of non-existent folder."""
    # Setup mock
    mock_notes_client.get_folder_info.return_value = None

    # Execute and verify
    with pytest.raises(ValueError, match="Folder 'Non-existent Folder' not found"):
        get_folder_info("Non-existent Folder")


def test_create_note_success(mock_notes_client):
    """Test successful note creation."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.create_note.return_value = mock_result

    # Execute
    result = create_note("New Note", "Note content", "Test Folder")

    # Verify
    assert result["success"] == True
    assert "created successfully" in result["message"]
    mock_notes_client.create_note.assert_called_once_with(
        "New Note", "Note content", "Test Folder"
    )


def test_create_note_without_folder(mock_notes_client):
    """Test successful note creation without specifying folder."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.create_note.return_value = mock_result

    # Execute
    result = create_note("New Note", "Note content")

    # Verify
    assert result["success"] == True
    assert "created successfully" in result["message"]
    mock_notes_client.create_note.assert_called_once_with(
        "New Note", "Note content", None
    )


def test_create_note_failure(mock_notes_client):
    """Test failed note creation."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Folder not found")
    mock_notes_client.create_note.return_value = mock_result

    # Execute
    result = create_note("New Note", "Note content", "Non-existent Folder")

    # Verify
    assert result["success"] == False
    assert "Failed to create note: Folder not found" == result["message"]


def test_list_notes_success(mock_notes_client):
    """Test successful listing of notes."""
    # Setup mock
    mock_notes_client.list_notes.return_value = ["Note 1", "Note 2", "Note 3"]

    # Execute
    result = list_notes()

    # Verify
    assert result["notes"] == ["Note 1", "Note 2", "Note 3"]
    assert "Found 3 notes" in result["message"]
    mock_notes_client.list_notes.assert_called_once_with(None)


def test_list_notes_in_folder(mock_notes_client):
    """Test listing notes in a specific folder."""
    # Setup mock
    mock_notes_client.list_notes.return_value = ["Note 1", "Note 2"]

    # Execute
    result = list_notes("Test Folder")

    # Verify
    assert result["notes"] == ["Note 1", "Note 2"]
    assert "in folder 'Test Folder'" in result["message"]
    mock_notes_client.list_notes.assert_called_once_with("Test Folder")


def test_list_notes_empty(mock_notes_client):
    """Test listing notes when no notes exist."""
    # Setup mock
    mock_notes_client.list_notes.return_value = []

    # Execute
    result = list_notes()

    # Verify
    assert result["notes"] == []
    assert result["message"] == "No notes found"
    mock_notes_client.list_notes.assert_called_once_with(None)


def test_update_note_content_success(mock_notes_client):
    """Test successful note content update."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.update_note_content.return_value = mock_result

    # Execute
    result = update_note_content("Test Note", "Updated content")

    # Verify
    assert result["success"] == True
    assert "content updated successfully" in result["message"]
    mock_notes_client.update_note_content.assert_called_once_with(
        "Test Note", "Updated content"
    )


def test_update_note_content_failure(mock_notes_client):
    """Test failed note content update."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Note not found")
    mock_notes_client.update_note_content.return_value = mock_result

    # Execute
    result = update_note_content("Non-existent Note", "Updated content")

    # Verify
    assert result["success"] == False
    assert "Failed to update note: Note not found" == result["message"]


def test_update_note_title_success(mock_notes_client):
    """Test successful note title update."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.update_note_title.return_value = mock_result

    # Execute
    result = update_note_title("Old Title", "New Title")

    # Verify
    assert result["success"] == True
    assert "Note title updated from 'Old Title' to 'New Title'" == result["message"]
    mock_notes_client.update_note_title.assert_called_once_with(
        "Old Title", "New Title"
    )


def test_update_note_title_failure(mock_notes_client):
    """Test failed note title update."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Note not found")
    mock_notes_client.update_note_title.return_value = mock_result

    # Execute
    result = update_note_title("Non-existent Note", "New Title")

    # Verify
    assert result["success"] == False
    assert "Failed to update note title: Note not found" == result["message"]


def test_create_folder_success(mock_notes_client):
    """Test successful folder creation."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.create_folder.return_value = mock_result

    # Execute
    result = create_folder("New Folder")

    # Verify
    assert result["success"] == True
    assert "Folder 'New Folder' created successfully" == result["message"]
    mock_notes_client.create_folder.assert_called_once_with("New Folder")


def test_create_folder_failure(mock_notes_client):
    """Test failed folder creation."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Folder already exists")
    mock_notes_client.create_folder.return_value = mock_result

    # Execute
    result = create_folder("Existing Folder")

    # Verify
    assert result["success"] == False
    assert "Failed to create folder: Folder already exists" == result["message"]


def test_list_folders_success(mock_notes_client):
    """Test successful listing of folders."""
    # Setup mock
    mock_notes_client.list_folders.return_value = ["Folder 1", "Folder 2", "Folder 3"]

    # Execute
    result = list_folders()

    # Verify
    assert result["folders"] == ["Folder 1", "Folder 2", "Folder 3"]
    assert "Found 3 folders" in result["message"]
    mock_notes_client.list_folders.assert_called_once()


def test_list_folders_empty(mock_notes_client):
    """Test listing folders when no folders exist."""
    # Setup mock
    mock_notes_client.list_folders.return_value = []

    # Execute
    result = list_folders()

    # Verify
    assert result["folders"] == []
    assert result["message"] == "No folders found"
    mock_notes_client.list_folders.assert_called_once()


def test_move_note_to_folder_success(mock_notes_client):
    """Test successful note movement to folder."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.move_note_to_folder.return_value = mock_result

    # Execute
    result = move_note_to_folder("Test Note", "Test Folder")

    # Verify
    assert result["success"] == True
    assert "Note 'Test Note' moved to folder 'Test Folder'" == result["message"]
    mock_notes_client.move_note_to_folder.assert_called_once_with(
        "Test Note", "Test Folder"
    )


def test_move_note_to_folder_failure(mock_notes_client):
    """Test failed note movement to folder."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Note or folder not found")
    mock_notes_client.move_note_to_folder.return_value = mock_result

    # Execute
    result = move_note_to_folder("Non-existent Note", "Non-existent Folder")

    # Verify
    assert result["success"] == False
    assert "Failed to move note: Note or folder not found" == result["message"]


def test_search_notes_success(mock_notes_client):
    """Test successful note search."""
    # Setup mock
    mock_notes_client.search_notes.return_value = ["Note 1", "Note 2", "Note 3"]

    # Execute
    result = search_notes("test")

    # Verify
    assert result["notes"] == ["Note 1", "Note 2", "Note 3"]
    assert "Found 3 notes containing 'test'" in result["message"]
    mock_notes_client.search_notes.assert_called_once_with("test")


def test_search_notes_no_matches(mock_notes_client):
    """Test note search with no matches."""
    # Setup mock
    mock_notes_client.search_notes.return_value = []

    # Execute
    result = search_notes("nonexistent")

    # Verify
    assert result["notes"] == []
    assert "No notes found containing 'nonexistent'" == result["message"]
    mock_notes_client.search_notes.assert_called_once_with("nonexistent")


def test_delete_note_success(mock_notes_client):
    """Test successful note deletion."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.delete_note.return_value = mock_result

    # Execute
    result = delete_note("Test Note")

    # Verify
    assert result["success"] == True
    assert "Note 'Test Note' deleted successfully" == result["message"]
    mock_notes_client.delete_note.assert_called_once_with("Test Note")


def test_delete_note_failure(mock_notes_client):
    """Test failed note deletion."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Note not found")
    mock_notes_client.delete_note.return_value = mock_result

    # Execute
    result = delete_note("Non-existent Note")

    # Verify
    assert result["success"] == False
    assert "Failed to delete note: Note not found" == result["message"]


def test_delete_folder_success(mock_notes_client):
    """Test successful folder deletion."""
    # Setup mock
    mock_result = AppleScriptResult(success=True)
    mock_notes_client.delete_folder.return_value = mock_result

    # Execute
    result = delete_folder("Test Folder")

    # Verify
    assert result["success"] == True
    assert "Folder 'Test Folder' deleted successfully" == result["message"]
    mock_notes_client.delete_folder.assert_called_once_with("Test Folder")


def test_delete_folder_failure(mock_notes_client):
    """Test failed folder deletion."""
    # Setup mock
    mock_result = AppleScriptResult(success=False, error="Folder not found")
    mock_notes_client.delete_folder.return_value = mock_result

    # Execute
    result = delete_folder("Non-existent Folder")

    # Verify
    assert result["success"] == False
    assert "Failed to delete folder: Folder not found" == result["message"]
