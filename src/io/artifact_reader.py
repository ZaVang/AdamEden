"""
src/io/artifact_reader.py — 圣物读取器（精简版）

渐进披露策略：不再一次性读取所有文件并推送给 LLM；
仅提供接口供 consciousness 层按需组装 state。
"""

import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("ADAM_DATA_DIR", "/app/data"))


def read_artifacts() -> dict:
    """
    返回基础 state 框架。
    Bible / Diary / error 等现在由 OracleClient 自行按需读取，
    这里只传递动态运行时信息（cmd_results 等）。
    """
    return {
        # cmd_results 由 consciousness / executor 层在每轮结束后填充
        "cmd_results": [],
    }
