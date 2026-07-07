from app.modules.trading.providers.ai.base_ai_provider import BaseAIProvider
from app.modules.trading.providers.ai.mock_ai_provider import MockAIProvider

_provider: BaseAIProvider = MockAIProvider()


def get_ai_provider() -> BaseAIProvider:
    return _provider


def set_ai_provider(provider: BaseAIProvider) -> None:
    """Replace the active provider at runtime. Call this at app startup to swap to OpenAI or Ollama."""
    global _provider
    _provider = provider
