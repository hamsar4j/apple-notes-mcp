from dataclasses import dataclass
from typing import Optional


@dataclass
class Note:
    name: str
    body: str
    folder: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None


@dataclass
class Folder:
    name: str
    note_count: Optional[int] = None


@dataclass
class AppleScriptResult:
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    return_code: Optional[int] = None
