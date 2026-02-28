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


class GeminiProvider(AIProvider):
    """Google Gemini - 完全免费且性能优秀"""

    API_BASE = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-exp"):
        """
        支持的模型：
        - gemini-2.0-flash-exp: 最新实验版，完全免费
        - gemini-1.5-flash: 快速版，$0.075/M
        - gemini-1.5-pro: 旗舰版，$1.25/M
        """
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        # Gemini API使用不同的消息格式，需要转换
        contents = []
        system_instruction = None

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                # Gemini使用 "user" 和 "model" 而不是 "user" 和 "assistant"
                role = "user" if msg["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

        request_body = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }

        if system_instruction:
            request_body["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/models/{self.model}:generateContent?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json=request_body
            )

            if response.status_code != 200:
                raise Exception(f"Gemini API错误: {response.text}")

            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]

    def get_name(self) -> str:
        return "Google Gemini"


class ClaudeProvider(AIProvider):
    """Anthropic Claude - 推理能力极强"""

    API_BASE = "https://api.anthropic.com/v1"

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-20241022"):
        """
        支持的模型：
        - claude-3-5-haiku-20241022: 快速版，$0.8/M input
        - claude-3-5-sonnet-20241022: 旗舰版，$3/M input
        - claude-3-opus-20240229: 最强版，$15/M input
        """
        super().__init__(api_key, model)

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        # Claude API需要分离system消息
        system_message = None
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        request_body = {
            "model": self.model,
            "messages": user_messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if system_message:
            request_body["system"] = system_message

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.API_BASE}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json=request_body
            )

            if response.status_code != 200:
                raise Exception(f"Claude API错误: {response.text}")

            result = response.json()
            return result["content"][0]["text"]

    def get_name(self) -> str:
        return "Anthropic Claude"


class OpenAIProvider(AIProvider):
    """OpenAI GPT - 业界标杆"""

    API_BASE = "https://api.openai.com/v1"

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        支持的模型：
        - gpt-4o-mini: 快速廉价，$0.15/M input
        - gpt-4o: 旗舰版，$2.5/M input
        - gpt-4-turbo: 旧版旗舰，$10/M input
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
                raise Exception(f"OpenAI API错误: {response.text}")

            result = response.json()
            return result["choices"][0]["message"]["content"]

    def get_name(self) -> str:
        return "OpenAI GPT"


class AIManager:
    """AI服务管理器 - 自动选择可用的provider"""

    def __init__(self):
        self.provider: Optional[AIProvider] = None
        self.all_providers: Dict[str, AIProvider] = {}  # 存储所有已配置的providers
        self._initialize_provider()

    def _initialize_provider(self):
        """
        按优先级初始化AI提供商：
        1. Gemini 2.0 Flash (完全免费，性能强)
        2. 智谱AI GLM-4-Flash (完全免费，国内访问)
        3. DeepSeek (极低成本)
        4. 通义千问 (廉价)
        5. Claude (推理强但贵)
        6. OpenAI GPT (贵)
        7. Groq (备选)
        """
        # 1. Gemini 2.0 Flash (完全免费，性能最强)
        gemini_key = os.getenv("GEMINI_API_KEY")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        if gemini_key:
            gemini_provider = GeminiProvider(gemini_key, model=gemini_model)
            self.all_providers["gemini"] = gemini_provider
            if not self.provider:
                self.provider = gemini_provider
                print(f"✓ 使用 Google Gemini {gemini_model} (完全免费)")

        # 2. 智谱AI GLM-4-Flash (完全免费，国内访问)
        zhipu_key = os.getenv("ZHIPU_API_KEY")
        zhipu_model = os.getenv("ZHIPU_MODEL", "glm-4-flash")
        if zhipu_key:
            zhipu_provider = ZhipuAIProvider(zhipu_key, model=zhipu_model)
            self.all_providers["zhipu"] = zhipu_provider
            if not self.provider:
                self.provider = zhipu_provider
                print(f"✓ 使用 智谱AI {zhipu_model} (完全免费)")

        # 3. DeepSeek (极低成本)
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        if deepseek_key:
            deepseek_provider = DeepSeekProvider(deepseek_key, model=deepseek_model)
            self.all_providers["deepseek"] = deepseek_provider
            if not self.provider:
                self.provider = deepseek_provider
                print(f"✓ 使用 DeepSeek {deepseek_model} (极低成本)")

        # 4. 通义千问
        qwen_key = os.getenv("QWEN_API_KEY")
        qwen_model = os.getenv("QWEN_MODEL", "qwen-turbo")
        if qwen_key:
            qwen_provider = QwenProvider(qwen_key, model=qwen_model)
            self.all_providers["qwen"] = qwen_provider
            if not self.provider:
                self.provider = qwen_provider
                print(f"✓ 使用 通义千问 {qwen_model}")

        # 5. Claude (推理能力强，但需要付费)
        claude_key = os.getenv("CLAUDE_API_KEY")
        claude_model = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022")
        if claude_key:
            claude_provider = ClaudeProvider(claude_key, model=claude_model)
            self.all_providers["claude"] = claude_provider
            if not self.provider:
                self.provider = claude_provider
                print(f"✓ 使用 Anthropic Claude {claude_model}")

        # 6. OpenAI GPT (贵，但性能稳定)
        openai_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if openai_key:
            openai_provider = OpenAIProvider(openai_key, model=openai_model)
            self.all_providers["openai"] = openai_provider
            if not self.provider:
                self.provider = openai_provider
                print(f"✓ 使用 OpenAI {openai_model}")

        # 7. Groq（备选，免费但可能被限）
        groq_key = os.getenv("GROQ_API_KEY")
        groq_model = os.getenv("GROQ_MODEL", "llama-3.2-90b-text-preview")
        if groq_key:
            groq_provider = GroqProvider(groq_key, model=groq_model)
            self.all_providers["groq"] = groq_provider
            if not self.provider:
                self.provider = groq_provider
                print(f"✓ 使用 Groq {groq_model} (免费)")

        if not self.provider:
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

    def get_all_providers_status(self) -> List[Dict]:
        """获取所有支持的AI模型及其配置状态"""
        all_models = [
            {
                "id": "gemini",
                "name": "Google Gemini",
                "model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
                "configured": "gemini" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, GeminiProvider),
                "cost": "免费",
                "description": "性能强，完全免费"
            },
            {
                "id": "zhipu",
                "name": "智谱AI (GLM-4)",
                "model": os.getenv("ZHIPU_MODEL", "glm-4-flash"),
                "configured": "zhipu" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, ZhipuAIProvider),
                "cost": "免费",
                "description": "中文理解强，国内访问"
            },
            {
                "id": "deepseek",
                "name": "DeepSeek",
                "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
                "configured": "deepseek" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, DeepSeekProvider),
                "cost": "极低成本",
                "description": "性价比极高"
            },
            {
                "id": "qwen",
                "name": "通义千问",
                "model": os.getenv("QWEN_MODEL", "qwen-turbo"),
                "configured": "qwen" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, QwenProvider),
                "cost": "廉价",
                "description": "阿里云，稳定快速"
            },
            {
                "id": "claude",
                "name": "Anthropic Claude",
                "model": os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022"),
                "configured": "claude" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, ClaudeProvider),
                "cost": "付费",
                "description": "推理能力最强"
            },
            {
                "id": "openai",
                "name": "OpenAI GPT",
                "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                "configured": "openai" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, OpenAIProvider),
                "cost": "付费",
                "description": "业界标杆"
            },
            {
                "id": "groq",
                "name": "Groq",
                "model": os.getenv("GROQ_MODEL", "llama-3.2-90b-text-preview"),
                "configured": "groq" in self.all_providers,
                "is_default": self.provider and isinstance(self.provider, GroqProvider),
                "cost": "免费",
                "description": "速度极快"
            }
        ]
        return all_models

    def use_provider(self, provider_id: str) -> bool:
        """临时切换到指定的provider"""
        if provider_id in self.all_providers:
            self.provider = self.all_providers[provider_id]
            return True
        return False

    def get_provider_id(self) -> str:
        """获取当前使用的provider ID"""
        for pid, provider in self.all_providers.items():
            if provider == self.provider:
                return pid
        return "unknown"

    async def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """发送对话请求"""
        if not self.provider:
            raise Exception("AI服务未配置，请设置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY")

        return await self.provider.chat(messages, temperature, max_tokens)


# 全局AI管理器实例
ai_manager = AIManager()
