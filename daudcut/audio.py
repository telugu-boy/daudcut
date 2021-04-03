import enum

class DACCodec(enum.Enum):
    WAV = 1
    VORBIS = 2
    MP3 = 3
    OPUS = 4

class DACAudio:
    """
    Provides a codec-agnostic wrapper for audio

    Attributes:
        codec (str): the encoding of the bytes-like object `audio`
        audio (bytes):
    """
    def __init__(self, codec: DACCodec, audio):
        self.codec = codec
        self.audio = audio


def http_get_audio(url, start=0, end=None):
    """
    Downloads audio from a provided URL with range options (rfc 2616 §14.35)

    Args:
        url: url to the content
        start: start of byte range if supported
        end: end of byte range if supported
    

    Returns:
        DACAudio object

    Raises:
        KeyError: Raises an exception.
    """
    pass
