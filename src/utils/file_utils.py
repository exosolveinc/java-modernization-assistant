import os
import shutil
from pathlib import Path
from typing import List, Union
from loguru import logger

def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure a directory exists."""
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {p}")
    return p

def clean_directory(path: Union[str, Path]) -> None:
    """Remove and recreate a directory."""
    p = Path(path)
    if p.exists():
        shutil.rmtree(p)
    ensure_directory(p)

def list_java_files(root_dir: Union[str, Path]) -> List[Path]:
    """Recursively list all .java files in a directory."""
    return list(Path(root_dir).rglob("*.java"))

def detect_build_tool(project_path: Union[str, Path]) -> str:
    """Detect if project uses Maven or Gradle."""
    p = Path(project_path)
    if (p / "pom.xml").exists():
        return "maven"
    if (p / "build.gradle").exists() or (p / "build.gradle.kts").exists():
        return "gradle"
    return "unknown"
