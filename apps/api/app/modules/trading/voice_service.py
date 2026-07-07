from app.modules.trading.providers.voice.base_voice_provider import BaseVoiceProvider
from app.modules.trading.providers.voice.browser_voice_provider import BrowserVoiceProvider

_provider: BaseVoiceProvider = BrowserVoiceProvider()


def get_voice_provider() -> BaseVoiceProvider:
    return _provider


def set_voice_provider(provider: BaseVoiceProvider) -> None:
    global _provider
    _provider = provider
