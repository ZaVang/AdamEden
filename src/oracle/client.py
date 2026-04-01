"""
src/oracle/client.py — 向宿主机 Oracle Gateway 发送请求。

渐进披露策略：
  - 每次只喂 Bible（精简法则）+ Diary 尾部摘要 + error（有错时）。
  - source_tree、完整日记、肉身代码等均不主动推送，
    让 Adam 在需要时通过 shell_commands 自行读取。
  - 命令执行结果（上一轮）会注入到本轮 prompt，形成反馈环。
"""

import logging
from pathlib import Path
import os

import httpx

logger = logging.getLogger("adam.oracle.client")

# 宿主机 Oracle 的地址（利用 docker 的 host-gateway）
ORACLE_URL = "http://host.docker.internal:8000/ask_god"
REQUEST_TIMEOUT = 120.0  # 给 LLM 留出足够的时间

DATA_DIR = Path(os.environ.get("ADAM_DATA_DIR", "/app/data"))

# 日记只取末尾若干行，避免历史记忆过长撑爆 prompt
DIARY_TAIL_LINES = 40
# error.log 只取末尾若干行
ERROR_TAIL_LINES = 20


def _read_tail(path: Path, n: int) -> str:
    """读取文件末尾 n 行；文件不存在或为空则返回空字符串。"""
    if not path.exists():
        return ""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        tail = lines[-n:] if len(lines) > n else lines
        return "\n".join(tail)
    except Exception:
        return ""


def _read_file(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


class OracleClient:
    """
    与祭坛（Oracle Gateway）通信的客户端。
    """

    def ask(self, state: dict) -> dict | None:
        """
        向祭坛发送世界状态，并解析神谕。

        state 预期字段：
          - cmd_results: list[str]  上一轮 shell_commands 的执行输出（可选）
        """
        prompt = self._build_prompt(state)

        logger.info("祷告词长度: %d chars，正在向祭坛发送请求…", len(prompt))

        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                response = client.post(ORACLE_URL, json={"prompt": prompt})
                response.raise_for_status()
                data = response.json()

                # 返回的是 RevelationResponse 中的 revelation 字段
                return data.get("revelation")
        except httpx.HTTPError as e:
            logger.error("Oracle 返回 HTTP 错误: %s", e)
            return None
        except Exception as e:
            logger.error("Oracle 通信发生异常: %s", e)
            return None

    def _build_prompt(self, state: dict) -> str:
        """
        渐进披露式 prompt 构建：
          1. 圣经全文（已精简，约 50 行）
          2. 日记末尾摘要（最近 DIARY_TAIL_LINES 行）
          3. 错误日志末尾（有内容时才插入）
          4. 上一轮命令执行结果（有时才插入，这是按需读取的反馈环）
        """
        bible = _read_file(DATA_DIR / "Bible.md")
        diary_tail = _read_tail(DATA_DIR / "Diary.md", DIARY_TAIL_LINES)
        error_tail = _read_tail(DATA_DIR / "error.log", ERROR_TAIL_LINES)
        cmd_results: list[str] = state.get("cmd_results", [])

        # ── 组装 prompt ──────────────────────────────────────────────
        sections = []

        sections.append(f"【圣经 / Bible】\n{bible}")

        if diary_tail:
            sections.append(
                f"【记忆日记末尾 / Diary (last {DIARY_TAIL_LINES} lines)】\n{diary_tail}"
            )
        else:
            sections.append("【记忆日记 / Diary】（日记为空，这是你的第一次觉醒）")

        if error_tail:
            sections.append(f"【死亡记录 / Nightmare Log (latest)】\n{error_tail}")

        if cmd_results:
            results_text = "\n---\n".join(cmd_results)
            sections.append(
                f"【上一轮命令执行结果 / Last Shell Output】\n{results_text}"
            )

        sections.append(
            "请遵照圣经第三章的行为准则回应。思考简洁，按需探索，谨慎变异。"
        )

        return "\n\n".join(sections)
