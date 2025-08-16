import subprocess
import logging
from .models import AppleScriptResult

logger = logging.getLogger(__name__)


class AppleScriptWrapper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def execute(self, script: str) -> AppleScriptResult:
        try:
            process = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            output = process.stdout.strip() if process.stdout else None
            error = process.stderr.strip() if process.stderr else None

            return AppleScriptResult(
                success=(process.returncode == 0),
                output=output,
                error=error,
                return_code=process.returncode,
            )

        except subprocess.TimeoutExpired:
            return AppleScriptResult(
                success=False, error=f"Timeout after {self.timeout}s", return_code=-1
            )

        except Exception as e:
            return AppleScriptResult(success=False, error=str(e), return_code=-1)

    def execute_notes_script(self, script: str) -> AppleScriptResult:
        full_script = f"""
        tell application "Notes"
            if not running then launch
            delay 1
            {script}
        end tell
        """
        return self.execute(full_script)

    def escape_string(self, text: str) -> str:
        if not text:
            return '""'
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
