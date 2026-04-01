"""
src/io/artifact_reader.py — 圣物读取器
"""

import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("ADAM_DATA_DIR", "/app/data"))

def read_artifacts() -> dict:
    """
    读取大天使挂载的所有圣物文件。
    """
    artifacts = {
        "bible": _read_file(DATA_DIR / "Bible.md"),
        "diary": _read_file(DATA_DIR / "Diary.md"),
        "error": _read_file(DATA_DIR / "error.log"),
    }
    
    # 还可以读取当前项目结构作为上下文
    artifacts["source_tree"] = _get_source_tree("/app")
    
    return artifacts

def _read_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def _get_source_tree(root_dir: str) -> str:
    tree = []
    for root, dirs, files in os.walk(root_dir):
        if ".git" in root or "__pycache__" in root:
            continue
        level = root.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * level
        tree.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            tree.append(f"{sub_indent}{f}")
    return "\n".join(tree)
