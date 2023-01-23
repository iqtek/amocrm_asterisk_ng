from enum import Enum


__all__ = ["Filetype"]


class Filetype(Enum):
    MP3 = "audio/mp3"
    MP4 = "audio/mp4"
    WAV = "audio/wav"
    WAVE = "audio/wave"
