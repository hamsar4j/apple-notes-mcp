import logging
from typing import Optional, List
from .applescript_wrapper import AppleScriptWrapper
from .models import Note, Folder, AppleScriptResult

logger = logging.getLogger(__name__)


class NotesClient:
    """Client for interacting with Apple Notes through AppleScript commands."""

    def __init__(self, timeout: int = 30) -> None:
        self.wrapper = AppleScriptWrapper(timeout=timeout)

    def _parse_list_output(self, output: Optional[str]) -> List[str]:
        """Parse a comma-separated list output from AppleScript."""
        if not output or not output.strip():
            return []
        return [item.strip() for item in output.split(",") if item.strip()]

    def create_note(
        self, title: str, content: str, folder_name: Optional[str] = None
    ) -> AppleScriptResult:
        title_esc = self.wrapper.escape_string(title)
        content_esc = self.wrapper.escape_string(content)

        if folder_name:
            folder_esc = self.wrapper.escape_string(folder_name)
            script = f"make new note in folder {folder_esc} with properties {{name:{title_esc}, body:{content_esc}}}"
        else:
            script = f"make new note with properties {{name:{title_esc}, body:{content_esc}}}"

        return self.wrapper.execute_notes_script(script)

    def list_notes(self, folder_name: Optional[str] = None) -> List[str]:
        if folder_name:
            folder_esc = self.wrapper.escape_string(folder_name)
            script = f"name of every note of folder {folder_esc}"
        else:
            script = "name of every note"

        result = self.wrapper.execute_notes_script(script)
        return self._parse_list_output(result.output) if result.success else []

    def get_note_content(self, note_name: str) -> Optional[Note]:
        name_esc = self.wrapper.escape_string(note_name)

        script = f"""
        repeat with n in notes
            if name of n is {name_esc} then
                set folder_name to ""
                try
                    set folder_name to name of container of n
                end try
                return name of n & "|||" & body of n & "|||" & folder_name
            end if
        end repeat
        """

        result = self.wrapper.execute_notes_script(script)

        if result.success and result.output:
            parts = result.output.split("|||", 2)
            if len(parts) >= 2:
                return Note(
                    name=parts[0],
                    body=parts[1],
                    folder=parts[2] if len(parts) > 2 and parts[2] else None,
                )

        return None

    def update_note_content(
        self, note_name: str, new_content: str
    ) -> AppleScriptResult:
        name_esc = self.wrapper.escape_string(note_name)
        content_esc = self.wrapper.escape_string(new_content)

        script = f"""
        repeat with n in notes
            if name of n is {name_esc} then
                set body of n to {content_esc}
                return "Updated"
            end if
        end repeat
        error "Note not found"
        """

        return self.wrapper.execute_notes_script(script)

    def update_note_title(self, old_name: str, new_name: str) -> AppleScriptResult:
        old_esc = self.wrapper.escape_string(old_name)
        new_esc = self.wrapper.escape_string(new_name)

        script = f"""
        repeat with n in notes
            if name of n is {old_esc} then
                set name of n to {new_esc}
                return "Updated"
            end if
        end repeat
        error "Note not found"
        """

        return self.wrapper.execute_notes_script(script)

    def search_notes(self, search_term: str) -> List[str]:
        term_esc = self.wrapper.escape_string(search_term.lower())
        script = f"""
        set matches to {{}}
        repeat with n in notes
            if (body of n contains {term_esc}) or (name of n contains {term_esc}) then
                set end of matches to name of n
            end if
        end repeat
        return matches
        """

        result = self.wrapper.execute_notes_script(script)
        return self._parse_list_output(result.output) if result.success else []

    def create_folder(self, folder_name: str) -> AppleScriptResult:
        name_esc = self.wrapper.escape_string(folder_name)

        script = f"""
        make new folder with properties {{name:{name_esc}}}
        return "Folder created successfully"
        """

        return self.wrapper.execute_notes_script(script)

    def list_folders(self) -> List[str]:
        result = self.wrapper.execute_notes_script("name of every folder")
        return self._parse_list_output(result.output) if result.success else []

    def get_folder_info(self, folder_name: str) -> Optional[Folder]:
        name_esc = self.wrapper.escape_string(folder_name)
        script = f"""
        repeat with f in folders
            if name of f is {name_esc} then
                return name of f & "|||" & (count of notes in f)
            end if
        end repeat
        """

        result = self.wrapper.execute_notes_script(script)
        if result.success and result.output:
            parts = result.output.split("|||")
            if len(parts) >= 2:
                try:
                    return Folder(name=parts[0], note_count=int(parts[1]))
                except ValueError:
                    return Folder(name=parts[0])
        return None

    def move_note_to_folder(
        self, note_name: str, folder_name: str
    ) -> AppleScriptResult:
        note_esc = self.wrapper.escape_string(note_name)
        folder_esc = self.wrapper.escape_string(folder_name)
        script = f"""
        repeat with n in notes
            if name of n is {note_esc} then
                move n to folder {folder_esc}
                return "Moved"
            end if
        end repeat
        error "Note not found"
        """
        return self.wrapper.execute_notes_script(script)

    def delete_note(self, note_name: str) -> AppleScriptResult:
        name_esc = self.wrapper.escape_string(note_name)
        script = f"delete note {name_esc}"
        return self.wrapper.execute_notes_script(script)
