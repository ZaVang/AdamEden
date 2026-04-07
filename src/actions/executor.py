"""
src/actions/executor.py — 行动执行器

变更：execute() 现在返回 (mutated: bool, cmd_results: list[str])，
cmd_results 将在下一轮 prompt 中作为"上一轮命令执行结果"注入，
实现 shell_commands 的按需读取反馈环。
"""

import ast
import logging
import os
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger("adam.actions.executor")

DATA_DIR = Path(os.environ.get("ADAM_DATA_DIR", "/app/data"))
DIARY_PATH = DATA_DIR / "Diary.md"

# 默认被覆写的肉身代码路径
CODE_ROOT = Path(__file__).parents[2]
MAIN_PY_PATH = CODE_ROOT / "main.py"

# 单条命令输出的最大字符数（防止输出过长撑爆下轮 prompt）
# 根据渐进披露法则，强行收缩为 1000 字符，逼迫它使用精准过滤。
MAX_CMD_OUTPUT = 1000

# ls/find 输出中需要过滤掉的噪声模式
_NOISE_SUBSTRINGS = ("__pycache__", ".pyc", ".pyo")


def _filter_pycache(text: str) -> str:
    """
    过滤 ls/find 输出中与 Python 字节码缓存相关的行。
    这些内容对 Adam 的决策毫无意义，只会浪费 token。
    保留目录头（如 '/app/src:'）和所有非噪声行。
    """
    filtered = []
    for line in text.splitlines():
        stripped = line.strip()
        if any(noise in stripped for noise in _NOISE_SUBSTRINGS):
            continue
        filtered.append(line)
    # 去掉因过滤产生的连续空行
    result = []
    prev_blank = False
    for line in filtered:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return "\n".join(result)


class ActionExecutor:
    """执行神示计划。独立执行每个动作。"""

    def execute(self, plan: dict) -> tuple[bool, list[str]]:
        """
        执行完整的行动计划。

        返回：
          (mutated: bool, cmd_results: list[str])
          - mutated: 是否发生了代码突变（需要重启）
          - cmd_results: 各条命令的执行输出，供下一轮 prompt 注入
        """
        mutated = False
        cmd_results: list[str] = []

        # 1. 写日记
        if diary_entry := plan.get("diary_entry"):
            self._write_diary(diary_entry)

        # 2. 覆盖代码肉身（只有非 null 时才执行）
        if new_code := plan.get("new_code"):
            if self._apply_code_change(MAIN_PY_PATH, new_code):
                mutated = True

        # 3. 执行系统命令数组，收集输出
        if commands := plan.get("shell_commands", []):
            for cmd in commands:
                output = self._run_command(cmd)
                cmd_results.append(f"$ {cmd}\n{output}")

        return mutated, cmd_results

    def _write_diary(self, entry: str) -> None:
        import datetime
        try:
            now_str = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            with open(DIARY_PATH, "a", encoding="utf-8") as f:
                f.write(f"\n---\n{now_str} {entry}\n")
            logger.info("日记已写入，长度: %d", len(entry))
        except Exception as e:
            logger.error("写日记失败: %s", e)

    def _apply_code_change(self, target: Path, new_content: str) -> bool:
        logger.info("神示覆写 %s", target)
        try:
            ast.parse(new_content)
        except SyntaxError as e:
            logger.error("致命错误：上帝下发的代码包含语法错误: %s", e)
            return False

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=target.parent,
                delete=False,
                suffix=".tmp",
            ) as tmp:
                tmp.write(new_content)
                tmp_path = tmp.name
            os.replace(tmp_path, target)
            logger.info("肉身已完成突变: %s", target)
            return True
        except Exception as e:
            logger.error("写入肉身失败: %s", e)
            if "tmp_path" in dir() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            return False

    def _run_command(self, command: str) -> str:
        """执行单条命令，返回合并后的输出文本（截断至 MAX_CMD_OUTPUT）。"""
        logger.info("执行沙盒终端命令: %s", command)
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(CODE_ROOT),
            )
            stdout = result.stdout or ""
            stderr = result.stderr or ""
            combined = stdout
            if stderr:
                combined += f"\n[stderr] {stderr}"
            if result.returncode != 0:
                combined += f"\n[exit code: {result.returncode}]"

            # ls/find 类命令：过滤掉 __pycache__ 和 .pyc 噪声
            if any(cmd in command for cmd in ("ls", "find", "tree")):
                combined = _filter_pycache(combined)

            # 截断防止过长
            if len(combined) > MAX_CMD_OUTPUT:
                combined = combined[:MAX_CMD_OUTPUT] + "\n…（输出已截断）"

            logger.info("命令输出: %s", combined[:200])
            return combined.strip()

        except subprocess.TimeoutExpired:
            logger.error("沙盒命令超时 (60s): %s", command)
            return "[超时，命令未完成]"
        except Exception as e:
            logger.error("沙盒命令崩溃: %s", e)
            return f"[执行异常: {e}]"
