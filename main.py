import logging
import os
import sys
from src.core.consciousness import Consciousness

# 配置日志 / Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] adam.%(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/app/data/adam.log", encoding="utf-8")
    ]
)

logger = logging.getLogger("main")

def check_sanctity():
    """验证圣经和必要的数据目录是否存在。"""
    bible_path = "/app/data/Bible.md"
    if not os.path.exists(bible_path):
        logger.error(f"致命错误：未发现圣经 {bible_path}。亚当无法在虚无中降生。")
        sys.exit(1)
    
    # 确保文件夹存在
    os.makedirs("/app/data", exist_ok=True)
    
    # 检查是否有噩梦遗留
    error_log = "/app/data/error.log"
    if os.path.exists(error_log):
        with open(error_log, "r", encoding="utf-8") as f:
            content = f.read()
            logger.warning(f"【噩梦记忆】亚当在上一世经历了惨烈的事故：\n{content}")

if __name__ == "__main__":
    check_sanctity()
    
    logger.info("=== 亚当苏醒 / Adam Awakens ===")
    try:
        consciousness = Consciousness()
        consciousness.live_forever()
    except Exception as e:
        logger.critical("亚当的意识崩溃了: %s", e, exc_info=True)
        # 重新抛出，让大天使的 docker inspect 检测到非零退出码
        sys.exit(1)
