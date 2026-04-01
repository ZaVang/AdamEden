"""
src/actions/executor.py — 行动执行器
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

class ActionExecutor:
    """执行神示计划。独立执行每个动作。"""

    def execute(self, plan: dict) -> bool:
        """
        执行完整的行动计划。
        返回布尔值：是否发生了代码突变（需要重启）。
        """
        mutated = False

        # 1. 写日记
        if diary_entry := plan.get("diary_entry"):
            self._write_diary(diary_entry)

        # 2. 覆盖代码肉身
        if new_code := plan.get("new_code"):
            if self._apply_code_change(MAIN_PY_PATH, new_code):
                mutated = True

        # 3. 执行系统命令数组
        if commands := plan.get("shell_commands", []):
            for cmd in commands:
                self._run_command(cmd)
        
        return mutated

    def _write_diary(self, entry: str) -> None:
        try:
            with open(DIARY_PATH, "a", encoding="utf-8") as f:
                f.write(f"\n---\n{entry}\n")
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
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, delete=False, suffix=".tmp") as tmp:
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

    def _run_command(self, command: str) -> None:
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
            if result.stdout:
                logger.info("输出: %s", result.stdout[:500])
            if result.stderr:
                logger.warning("错出: %s", result.stderr[:500])
            if result.returncode != 0:
                logger.warning("命令退出码异常: %d", result.returncode)
        except subprocess.TimeoutExpired:
            logger.error("沙盒命令超时 (60s): %s", command)
        except Exception as e:
            logger.error("沙盒命令奔溃: %s", e)
