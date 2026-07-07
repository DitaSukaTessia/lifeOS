"""
ElevenLabs TTS provider.

Activation:
  1. Add ELEVENLABS_API_KEY=<your-key> to apps/api/.env
  2. Set elevenlabs_api_key in config.py
  3. Wire in main.py voice provider setup

Returns audio as a base64 data URI (audio/mpeg) so no file storage is needed.
"""
import base64
import logging

import httpx

from app.modules.trading.providers.voice.base_voice_provider import BaseVoiceProvider, VoiceAudioData

log = logging.getLogger(__name__)

_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
_DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel — neutral, clear


class ElevenLabsProvider(BaseVoiceProvider):

    def __init__(self, api_key: str, voice_id: str = _DEFAULT_VOICE_ID):
        self._api_key = api_key
        self._voice_id = voice_id

    @property
    def provider_name(self) -> str:
        return "elevenlabs"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    async def speak(self, text: str) -> VoiceAudioData:
        url = _API_URL.format(voice_id=self._voice_id)
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers={"xi-api-key": self._api_key, "Content-Type": "application/json"},
                json={"text": text, "model_id": "eleven_turbo_v2"},
            )
            response.raise_for_status()
            audio_b64 = base64.b64encode(response.content).decode()
        return VoiceAudioData(
            provider=self.provider_name,
            text=text,
            audio_url=f"data:audio/mpeg;base64,{audio_b64}",
        )
