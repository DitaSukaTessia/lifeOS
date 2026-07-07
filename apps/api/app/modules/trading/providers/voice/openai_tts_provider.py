"""
OpenAI TTS provider (tts-1 / tts-1-hd).

Activation:
  1. Add OPENAI_API_KEY=<your-key> to apps/api/.env
  2. Set openai_api_key in config.py
  3. Wire in main.py voice provider setup

Returns audio as a base64 data URI (audio/mpeg).
"""
import base64
import logging

from app.modules.trading.providers.voice.base_voice_provider import BaseVoiceProvider, VoiceAudioData

log = logging.getLogger(__name__)


class OpenAITTSProvider(BaseVoiceProvider):

    def __init__(self, api_key: str, model: str = "tts-1", voice: str = "onyx"):
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise ImportError(
                "openai package is required for OpenAITTSProvider. "
                "Install it with: pip install openai"
            ) from exc
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._voice = voice

    @property
    def provider_name(self) -> str:
        return f"openai_tts/{self._model}"

    @property
    def is_available(self) -> bool:
        return bool(self._client.api_key)

    async def speak(self, text: str) -> VoiceAudioData:
        response = await self._client.audio.speech.create(
            model=self._model,
            voice=self._voice,  # type: ignore[arg-type]
            input=text,
        )
        audio_bytes = response.content
        audio_b64 = base64.b64encode(audio_bytes).decode()
        return VoiceAudioData(
            provider=self.provider_name,
            text=text,
            audio_url=f"data:audio/mpeg;base64,{audio_b64}",
        )
