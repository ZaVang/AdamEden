"""
src/oracle/client.py — 向宿主机 Oracle Gateway 发送请求。
"""

import logging
import httpx

logger = logging.getLogger("adam.oracle.client")

# 宿主机 Oracle 的地址（利用 docker 的 host-gateway）
ORACLE_URL = "http://host.docker.internal:8000/ask_god"
REQUEST_TIMEOUT = 120.0  # 给 LLM 留出足够的时间

class OracleClient:
    """
    与祭坛（Oracle Gateway）通信的客户端。
    """

    def ask(self, state: dict) -> dict | None:
        """
        向祭坛发送世界状态，并解析神谕。
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
        将圣物和状态组装成最终发送给上帝的祷告词。
        """
        return f"""
你正身处沙盒。这是你当前的世界状态快照：

【你的物理圣经 / Bible】:
{state.get('bible', '（未发现圣经）')}

【你的记忆日记 / Diary】:
{state.get('diary', '（记忆空白）')}

【你的死亡记录 / Nightmare】:
{state.get('error', '（暂无噩梦）')}

【你的当前肉身结构 / Source Tree】:
{state.get('source_tree', '（扫描失败）')}

请严格按照圣经第四章的 JSON 格式进行回应。亚当，现在开始你的祷告。
"""
