"""
Browser TTS provider — delegates synthesis to the Web Speech API on the frontend.

The backend returns the script text and duration estimate; the browser reads it aloud.
No API keys required. Works immediately out of the box.
"""
from app.modules.trading.providers.voice.base_voice_provider import BaseVoiceProvider, VoiceAudioData

_WORDS_PER_MINUTE = 150


class BrowserVoiceProvider(BaseVoiceProvider):

    @property
    def provider_name(self) -> str:
        return "browser"

    @property
    def is_available(self) -> bool:
        return True

    async def speak(self, text: str) -> VoiceAudioData:
        word_count = len(text.split())
        duration = round((word_count / _WORDS_PER_MINUTE) * 60, 1)
        return VoiceAudioData(
            provider=self.provider_name,
            text=text,
            audio_url=None,
            duration_estimate_seconds=duration,
        )
