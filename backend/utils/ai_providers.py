"""
AI服务提供商统一接口

支持多个AI提供商：
- DeepSeek (推荐，极低成本)
- 智谱AI (GLM-4，免费额度)
- 通义千问 (阿里云)
- Groq (免费，超快)
"""
import os
import httpx
from typing import Optional, List, Dict
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """AI提供商基类"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """发送对话请求"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取提供商名称"""
        pass


class DeepSeekProvider(AIProvider):
    """DeepSeek AI - 性价比之王"""

    API_BASE = "https://api.deepseek.com/v1"

    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise Exception(f"DeepSeek API错误: {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]

    def get_name(self) -> str:
        return "DeepSeek"


class ZhipuAIProvider(AIProvider):
    """智谱AI (GLM-4) - 中文理解优秀"""

    API_BASE = "https://open.bigmodel.cn/api/paas/v4"

    def __init__(self, api_key: str, model: str = "glm-4-flash"):
        """
        支持的模型：
        - glm-4-flash: 完全免费！无限制 (推荐日常使用)
        - glm-4-air: 均衡版 (1元/M tokens)
        - glm-4-plus: 旗舰版 (50元/M tokens)
        """
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise Exception(f"智谱AI API错误: {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]

    def get_name(self) -> str:
        return "智谱AI (GLM-4)"


class QwenProvider(AIProvider):
    """通义千问 - 阿里云"""

    API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    def __init__(self, api_key: str, model: str = "qwen-turbo"):
        """
        支持的模型：
        - qwen-turbo: 快速廉价 (0.3元/M input)
        - qwen-plus: 增强版 (4元/M input)
        - qwen-max: 最强版 (20元/M input)
        - qwen-long: 长文本 (0.5元/M input, 1M tokens上下文)
        """
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise Exception(f"通义千问 API错误: {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]

    def get_name(self) -> str:
        return "通义千问"


class GroqProvider(AIProvider):
    """Groq - 免费且超快"""

    API_BASE = "https://api.groq.com/openai/v1"

    def __init__(self, api_key: str, model: str = "llama-3.2-90b-text-preview"):
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            )

            if response.status_code != 200:
                raise Exception(f"Groq API错误: {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]

    def get_name(self) -> str:
        return "Groq"


class AIManager:
    """AI服务管理器 - 自动选择可用的provider"""

    def __init__(self):
        self.provider: Optional[AIProvider] = None
        self._initialize_provider()

    def _initialize_provider(self):
        """
        按优先级初始化AI提供商：
        1. 智谱AI GLM-4-Flash (完全免费！)
        2. DeepSeek (极低成本)
        3. 通义千问 Qwen-Turbo (廉价)
        4. Groq (备选，免费但可能被限制)
        """
        # 1. 优先使用智谱AI GLM-4-Flash (完全免费！)
        zhipu_key = os.getenv("ZHIPU_API_KEY")
        if zhipu_key:
            self.provider = ZhipuAIProvider(zhipu_key, model="glm-4-flash")
            print("✓ 使用 智谱AI GLM-4-Flash (完全免费)")
            return

        # 2. 尝试DeepSeek (极低成本)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key:
            self.provider = DeepSeekProvider(deepseek_key)
            print("✓ 使用 DeepSeek-V3 (极低成本)")
            return

        # 3. 尝试通义千问
        qwen_key = os.getenv("QWEN_API_KEY")
        qwen_model = os.getenv("QWEN_MODEL", "qwen-turbo")  # 支持自定义模型
        if qwen_key:
            self.provider = QwenProvider(qwen_key, model=qwen_model)
            print(f"✓ 使用 通义千问 {qwen_model}")
            return

        # 4. 尝试Groq（备选）
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            self.provider = GroqProvider(groq_key)
            print("✓ 使用 Groq (免费)")
            return

        print("⚠️  未配置任何AI服务")

    def is_configured(self) -> bool:
        """检查是否配置了AI服务"""
        return self.provider is not None

    def get_provider_name(self) -> str:
        """获取当前使用的提供商名称"""
        if self.provider:
            return self.provider.get_name()
        return "未配置"

    def get_model_name(self) -> str:
        """获取当前使用的模型名称"""
        if self.provider:
            return self.provider.model
        return "未配置"

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """发送对话请求"""
        if not self.provider:
            raise Exception("AI服务未配置，请设置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY")

        return await self.provider.chat(messages, temperature, max_tokens)


# 全局AI管理器实例
ai_manager = AIManager()
