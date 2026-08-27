"""
File and path utilities for the PQ Assistant.

Provides reusable helpers for file handling, directory management,
path validation, and basic file operations.
"""

from pathlib import Path
from typing import Iterable, Optional


def ensure_directory(directory: str | Path) -> Path:
    """
    Create a directory if it does not already exist.

    Args:
        directory: Directory path.

    Returns:
        Path object representing the directory.
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_exists(file_path: str | Path) -> bool:
    """
    Check whether a path exists and is a file.

    Args:
        file_path: Path to the file.

    Returns:
        True if the file exists, otherwise False.
    """
    return Path(file_path).is_file()


def directory_exists(directory: str | Path) -> bool:
    """
    Check whether a path exists and is a directory.

    Args:
        directory: Directory path.

    Returns:
        True if the directory exists, otherwise False.
    """
    return Path(directory).is_dir()


def get_file_extension(file_path: str | Path) -> str:
    """
    Get the file extension.

    Args:
        file_path: Path to the file.

    Returns:
        File extension including the dot, in lowercase.
    """
    return Path(file_path).suffix.lower()


def get_file_name(file_path: str | Path) -> str:
    """
    Get the file name from a path.

    Args:
        file_path: Path to the file.

    Returns:
        File name.
    """
    return Path(file_path).name


def get_file_stem(file_path: str | Path) -> str:
    """
    Get the file name without its extension.

    Args:
        file_path: Path to the file.

    Returns:
        File stem.
    """
    return Path(file_path).stem


def get_file_size(file_path: str | Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to the file.

    Returns:
        File size in bytes, or 0 if the file does not exist.
    """
    path = Path(file_path)

    if not path.is_file():
        return 0

    return path.stat().st_size


def read_text_file(
    file_path: str | Path,
    encoding: str = "utf-8",
    default: str = "",
) -> str:
    """
    Read text content from a file.

    Args:
        file_path: Path to the file.
        encoding: File encoding.
        default: Value returned if reading fails.

    Returns:
        File contents or default value.
    """
    path = Path(file_path)

    try:
        return path.read_text(encoding=encoding)
    except (OSError, UnicodeDecodeError):
        return default


def write_text_file(
    file_path: str | Path,
    content: str,
    encoding: str = "utf-8",
) -> bool:
    """
    Write text content to a file.

    Parent directories are created automatically.

    Args:
        file_path: Destination file path.
        content: Text content.
        encoding: File encoding.

    Returns:
        True if successful, otherwise False.
    """
    path = Path(file_path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)
        return True
    except OSError:
        return False


def list_files(
    directory: str | Path,
    extensions: Optional[Iterable[str]] = None,
    recursive: bool = False,
) -> list[Path]:
    """
    List files inside a directory.

    Args:
        directory: Directory to search.
        extensions: Optional file extensions to filter by.
        recursive: Whether to search subdirectories.

    Returns:
        List of matching file paths.
    """
    path = Path(directory)

    if not path.is_dir():
        return []

    normalized_extensions = None

    if extensions:
        normalized_extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in extensions
        }

    pattern = "**/*" if recursive else "*"

    files = [
        item
        for item in path.glob(pattern)
        if item.is_file()
    ]

    if normalized_extensions:
        files = [
            item
            for item in files
            if item.suffix.lower() in normalized_extensions
        ]

    return sorted(files)


def delete_file(file_path: str | Path) -> bool:
    """
    Delete a file if it exists.

    Args:
        file_path: Path to the file.

    Returns:
        True if deleted successfully, otherwise False.
    """
    path = Path(file_path)

    try:
        if path.is_file():
            path.unlink()
            return True
        return False
    except OSError:
        return False


def resolve_path(
    file_path: str | Path,
    base_directory: Optional[str | Path] = None,
) -> Path:
    """
    Resolve a path into an absolute path.

    Args:
        file_path: Input file path.
        base_directory: Optional base directory for relative paths.

    Returns:
        Resolved absolute Path.
    """
    path = Path(file_path)

    if not path.is_absolute() and base_directory is not None:
        path = Path(base_directory) / path

    return path.expanduser().resolve()