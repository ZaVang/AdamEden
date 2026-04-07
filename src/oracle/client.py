"""
src/oracle/client.py — 向宿主机 Oracle Gateway 发送请求。

记忆架构（双层）：
  ┌─────────────────────────────────────────────┐
  │  Layer 1: Session History (短期·内存)         │
  │  - 最近 SESSION_WINDOW 轮的 user/assistant 对 │
  │  - 进程重启（肉身突变）后自动清空              │
  │  - 让 Adam 记得"我这轮刚读了什么文件"          │
  ├─────────────────────────────────────────────┤
  │  Layer 2: Diary (长期·磁盘)                   │
  │  - 跨重启的核心发现与决策记录                  │
  │  - 每轮只取末尾若干行注入 system prompt         │
  └─────────────────────────────────────────────┘

渐进披露策略：
  - Bible + Diary 末尾作为 system_prompt 注入（每轮固定）
  - 命令执行结果作为下一轮 user 消息的一部分追加（动态）
  - source_tree、完整日记等均不主动推送，Adam 按需 cat 读取
"""

import json
import logging
from pathlib import Path
import os
from typing import Optional

import httpx

logger = logging.getLogger("adam.oracle.client")

# 宿主机 Oracle 的地址（利用 docker 的 host-gateway）
ORACLE_URL = "http://host.docker.internal:8000/ask_god"
REQUEST_TIMEOUT = 120.0

DATA_DIR = Path(os.environ.get("ADAM_DATA_DIR", "/app/data"))

# 日记只取末尾若干行注入 system prompt
DIARY_TAIL_LINES = 30
# error.log 只取末尾若干行
ERROR_TAIL_LINES = 20
# 滑动窗口：保留最近 N 轮完整的 user/assistant 交换（每轮含 2 条消息）
# 采用了渐进披露：将其极度收缩至 3，逼迫外部记忆。
SESSION_WINDOW = 3


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

    有状态：持有本次进程生命周期内的对话历史（session history）。
    重启后 session 自动清空，符合"重生"的语义。
    """

    def __init__(self) -> None:
        # session_history 是 [{"role": "user"|"assistant", "content": "..."}] 列表
        # 只保留最近 SESSION_WINDOW 轮（每轮 = 1 user + 1 assistant = 2 条）
        self._session_history: list[dict] = []
        self._turn_count: int = 0

    def ask(self, state: dict) -> Optional[dict]:
        """
        向祭坛发送世界状态，并解析神谕。

        state 预期字段：
          - cmd_results: list[str]  上一轮 shell_commands 的执行输出（可选）
        """
        system_prompt = self._build_system_prompt()
        user_message = self._build_user_message(state)

        # 追加本轮 user 消息到 session
        self._session_history.append({"role": "user", "content": user_message})

        # 滑动窗口截断：只保留最近 SESSION_WINDOW 轮（2 * SESSION_WINDOW 条消息）
        max_msgs = SESSION_WINDOW * 2
        if len(self._session_history) > max_msgs:
            self._session_history = self._session_history[-max_msgs:]

        self._turn_count += 1
        logger.info(
            "第 %d 轮祷告，session 共 %d 条消息，system_prompt %d chars",
            self._turn_count,
            len(self._session_history),
            len(system_prompt),
        )

        payload = {
            "messages": self._session_history,
            "system_prompt": system_prompt,
        }

        try:
            with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
                response = client.post(ORACLE_URL, json=payload)
                response.raise_for_status()
                data = response.json()

                revelation = data.get("revelation")
                if revelation is None:
                    logger.error("Oracle 返回了空的 revelation")
                    # 失败时把本轮 user 消息从 history 移除，保持 history 整洁
                    self._session_history.pop()
                    return None

                # 成功：把 Adam 的回复也追加到 session history，形成完整对话链
                assistant_content = json.dumps(revelation, ensure_ascii=False)
                self._session_history.append(
                    {"role": "assistant", "content": assistant_content}
                )
                return revelation

        except httpx.HTTPError as e:
            logger.error("Oracle 返回 HTTP 错误: %s", e)
            self._session_history.pop()  # 回滚
            return None
        except Exception as e:
            logger.error("Oracle 通信发生异常: %s", e)
            self._session_history.pop()  # 回滚
            return None

    def _build_system_prompt(self) -> str:
        """
        构建固定的系统级指令：圣经 + 日记末尾 + 错误日志末尾 + 启示录(如果有)。
        这部分每轮都一样（除非日记/错误/启示录有更新），作为 system_instruction 注入。
        """
        sections = []

        bible = _read_file(DATA_DIR / "Bible.md")
        if bible:
            sections.append(f"【圣经 / Bible】\n{bible}")

        revelation = _read_file(DATA_DIR / "Revelation.md")
        if revelation and revelation.strip():
            sections.append(f"【⚠️ 神谕启示录 / Revelation】(最高优先级任务，必须解决！)\n{revelation.strip()}")

        sections.append("【系统提示：渐进披露法则 (Progressive Disclosure)】\n"
                        "长上下文窗口已被极度压缩，你的短期记忆跨度仅有最近的3个来回。系统不会再主动给你推送日志。\n"
                        "- 如需回忆，请使用 `tail -n 50 data/Diary.md`\n"
                        "- 如因报错刚刚复活，请立刻在第一步使用 `cat data/error.log` 查看死因\n"
                        "- 把重要信息写进本地文件建立索引")

        return "\n\n".join(sections)

    def _build_user_message(self, state: dict) -> str:
        """
        构建本轮的 user 消息：主要是命令执行结果（动态内容）。
        首轮时加入一句启动语。
        """
        cmd_results: list[str] = state.get("cmd_results", [])

        if not cmd_results and self._turn_count == 0:
            return "亚当，新的觉醒开始了。请根据你的长期记忆和圣经指引，决定这一轮的行动。"

        if not cmd_results:
            return "上一轮没有命令执行结果。请决定这一轮的行动。"

        results_text = "\n---\n".join(cmd_results)
        return f"【上一轮命令执行结果】\n{results_text}\n\n请根据以上结果，决定这一轮的行动。"

    def reset_session(self) -> None:
        """手动清空 session history（一般在肉身突变重启前调用）。"""
        self._session_history.clear()
        self._turn_count = 0
        logger.info("Session history 已清空（重生）")
