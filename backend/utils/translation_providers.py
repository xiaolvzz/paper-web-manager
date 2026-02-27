"""
翻译服务提供商统一接口

支持多个翻译服务：
- DeepL (质量最好)
- 有道翻译 (国内首选)
- 百度翻译 (国内备选)
- 彩云小译 (中英专注)
- Google Translate (免费无需注册)
"""
import os
import httpx
import hashlib
import uuid
import time
from typing import Optional
from abc import ABC, abstractmethod


class TranslationProvider(ABC):
    """翻译提供商基类"""

    @abstractmethod
    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        """翻译文本"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取提供商名称"""
        pass


class DeepLProvider(TranslationProvider):
    """DeepL - 翻译质量最好"""

    API_BASE = "https://api-free.deepl.com/v2"  # 免费版API

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        # DeepL语言代码转换
        lang_map = {
            "zh": "ZH",
            "en": "EN-US",
            "ja": "JA",
            "ko": "KO",
            "fr": "FR",
            "de": "DE",
            "es": "ES",
            "ru": "RU",
            "auto": None  # DeepL自动检测
        }

        target = lang_map.get(target_lang, "ZH")
        source = lang_map.get(source_lang)

        async with httpx.AsyncClient(timeout=30.0) as client:
            data = {
                "auth_key": self.api_key,
                "text": text,
                "target_lang": target
            }
            if source:
                data["source_lang"] = source

            response = await client.post(
                f"{self.API_BASE}/translate",
                data=data
            )

            if response.status_code != 200:
                raise Exception(f"DeepL API错误: {response.text}")

            result = response.json()
            return result["translations"][0]["text"]

    def get_name(self) -> str:
        return "DeepL"


class YoudaoProvider(TranslationProvider):
    """有道智云翻译 - 国内首选"""

    API_BASE = "https://openapi.youdao.com/api"

    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key

    def _generate_sign(self, query: str, salt: str) -> str:
        """生成签名"""
        sign_str = self.app_id + query + salt + self.app_key
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        # 有道语言代码
        lang_map = {
            "zh": "zh-CHS",
            "en": "en",
            "ja": "ja",
            "ko": "ko",
            "fr": "fr",
            "de": "de",
            "es": "es",
            "ru": "ru",
            "auto": "auto"
        }

        salt = str(uuid.uuid4())
        sign = self._generate_sign(text, salt)

        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "q": text,
                "from": lang_map.get(source_lang, "auto"),
                "to": lang_map.get(target_lang, "zh-CHS"),
                "appKey": self.app_id,
                "salt": salt,
                "sign": sign,
                "signType": "v3",
                "curtime": str(int(time.time()))
            }

            response = await client.get(self.API_BASE, params=params)

            if response.status_code != 200:
                raise Exception(f"有道翻译API错误: {response.text}")

            result = response.json()
            if result.get("errorCode") != "0":
                raise Exception(f"有道翻译错误: {result.get('errorCode')}")

            return result["translation"][0]

    def get_name(self) -> str:
        return "有道翻译"


class BaiduProvider(TranslationProvider):
    """百度翻译 - 国内备选"""

    API_BASE = "https://fanyi-api.baidu.com/api/trans/vip/translate"

    def __init__(self, app_id: str, app_key: str):
        self.app_id = app_id
        self.app_key = app_key

    def _generate_sign(self, query: str, salt: str) -> str:
        """生成签名"""
        sign_str = self.app_id + query + salt + self.app_key
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        salt = str(int(time.time() * 1000))
        sign = self._generate_sign(text, salt)

        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "q": text,
                "from": source_lang,
                "to": target_lang,
                "appid": self.app_id,
                "salt": salt,
                "sign": sign
            }

            response = await client.get(self.API_BASE, params=params)

            if response.status_code != 200:
                raise Exception(f"百度翻译API错误: {response.text}")

            result = response.json()
            if "error_code" in result:
                raise Exception(f"百度翻译错误: {result.get('error_code')}")

            return "\n".join([item["dst"] for item in result["trans_result"]])

    def get_name(self) -> str:
        return "百度翻译"


class CaiyunProvider(TranslationProvider):
    """彩云小译 - 中英专注"""

    API_BASE = "https://api.interpreter.caiyunai.com/v1/translator"

    def __init__(self, token: str):
        self.token = token

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        # 彩云只支持中英互译
        if source_lang == "auto":
            # 简单检测：包含中文则翻译成英文，否则翻译成中文
            source = "zh" if any('\u4e00' <= c <= '\u9fff' for c in text) else "en"
            target = "en" if source == "zh" else "zh"
        else:
            source = source_lang
            target = target_lang

        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "source": text.split('\n'),
                "trans_type": f"{source}2{target}",
                "request_id": "demo",
                "detect": True
            }

            response = await client.post(
                self.API_BASE,
                headers={
                    "content-type": "application/json",
                    "x-authorization": f"token {self.token}"
                },
                json=payload
            )

            if response.status_code != 200:
                raise Exception(f"彩云小译API错误: {response.text}")

            result = response.json()
            return "\n".join(result["target"])

    def get_name(self) -> str:
        return "彩云小译"


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate (非官方) - 完全免费"""

    API_BASE = "https://translate.googleapis.com/translate_a/single"

    def __init__(self):
        pass

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "client": "gtx",
                "sl": source_lang,
                "tl": target_lang,
                "dt": "t",
                "q": text
            }

            response = await client.get(self.API_BASE, params=params)

            if response.status_code != 200:
                raise Exception(f"Google翻译错误: {response.text}")

            result = response.json()
            # 解析响应格式：[[["翻译文本", "原文", null, null, 10]], ...]
            translated = ""
            for item in result[0]:
                if item[0]:
                    translated += item[0]

            return translated

    def get_name(self) -> str:
        return "Google翻译"


class TranslationManager:
    """翻译服务管理器 - 自动选择可用的provider"""

    def __init__(self):
        self.provider: Optional[TranslationProvider] = None
        self._initialize_provider()

    def _initialize_provider(self):
        """
        按优先级初始化翻译提供商：
        1. DeepL (质量最好)
        2. 有道翻译 (国内首选)
        3. 百度翻译 (国内备选)
        4. 彩云小译 (中英专注)
        5. Google翻译 (完全免费，无需配置)
        """
        # 1. 尝试DeepL
        deepl_key = os.getenv("DEEPL_API_KEY")
        if deepl_key:
            self.provider = DeepLProvider(deepl_key)
            print("✓ 使用 DeepL 翻译服务 (质量最好)")
            return

        # 2. 尝试有道翻译
        youdao_app_id = os.getenv("YOUDAO_APP_ID")
        youdao_key = os.getenv("YOUDAO_API_KEY")
        if youdao_app_id and youdao_key:
            self.provider = YoudaoProvider(youdao_app_id, youdao_key)
            print("✓ 使用 有道翻译服务 (国内首选)")
            return

        # 3. 尝试百度翻译
        baidu_app_id = os.getenv("BAIDU_TRANSLATE_APPID")
        baidu_key = os.getenv("BAIDU_TRANSLATE_KEY")
        if baidu_app_id and baidu_key:
            self.provider = BaiduProvider(baidu_app_id, baidu_key)
            print("✓ 使用 百度翻译服务")
            return

        # 4. 尝试彩云小译
        caiyun_token = os.getenv("CAIYUN_TOKEN")
        if caiyun_token:
            self.provider = CaiyunProvider(caiyun_token)
            print("✓ 使用 彩云小译服务")
            return

        # 5. 使用Google翻译（无需配置）
        self.provider = GoogleTranslateProvider()
        print("✓ 使用 Google翻译服务 (免费无需配置)")

    def is_configured(self) -> bool:
        """检查是否配置了翻译服务"""
        return self.provider is not None

    def get_provider_name(self) -> str:
        """获取当前使用的提供商名称"""
        if self.provider:
            return self.provider.get_name()
        return "未配置"

    async def translate(self, text: str, source_lang: str = "auto", target_lang: str = "zh") -> str:
        """翻译文本"""
        if not self.provider:
            raise Exception("翻译服务未配置")

        return await self.provider.translate(text, source_lang, target_lang)


# 全局翻译管理器实例
translation_manager = TranslationManager()
