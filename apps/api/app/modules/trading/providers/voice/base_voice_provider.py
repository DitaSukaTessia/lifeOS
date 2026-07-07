from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class VoiceAudioData:
    provider: str
    text: str
    audio_url: Optional[str] = None          # None = browser handles TTS; data URI for cloud providers
    duration_estimate_seconds: Optional[float] = None


class BaseVoiceProvider(ABC):

    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @property
    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    async def speak(self, text: str) -> VoiceAudioData: ...
