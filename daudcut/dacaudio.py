"""
    Discord Audio Cutter
    Copyright (C) 2021 telugu_boy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


"""
General purpose audio cutting with re-encoding
Format specific methods will be available in their own modules
"""

import enum
import ffmpeg
from urllib.request import Request, urlopen
from urllib.parse import unquote
import magic
import logging
import re

logger = logging.getLogger("daudcut")
# This header is needed or else we get 403 forbidden '-'
# The user agent and accept* are copied from a random Chrome request
# stolen from my discord server exporter project
req_hdr = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


class DACCodec(enum.Enum):
    WAVE = 1
    VORBIS = 2
    MP3 = 3


# mime subtype to DACCodec
mimest2daccodec = {"x-wav": DACCodec.WAVE, "ogg": DACCodec.VORBIS, "mpeg": DACCodec.MP3}


class DACAudio:
    """
    Provides a codec-agnostic wrapper for audia

    Attributes:
        codec (str): the mime type of the bytes-like object `audio`
        audio (bytes): the actual audio data
    """

    def __init__(self, codec: DACCodec, audio: bytes):
        self.codec = codec
        self.audio = audio


def conv_mime_daccodec(mime: str) -> DACCodec:
    typ, subtype = mime.split("/")

    # make sure that we are working with audio
    assert typ == "audio"

    return mimest2daccodec[subtype]


def get_daccodec_from_buf(buf: bytes):
    mime = magic.from_buffer(buf, mime=True)
    return conv_mime_daccodec(mime)


def http_get_audio(url):
    """
    Downloads an entire audio file given url

    Args:
        url: url to the content
        start: start of byte range if supported
        end: end of byte range if supported

    Returns:
        DACAudio object
    """

    req = Request(url, None, req_hdr)
    file_req = urlopen(req)
    file_req_info = file_req.info()

    # Content-Disposition header looks like `Content-Disposition: attachment;%20filename=test_audio.wav`
    dec_disposition = unquote(file_req_info["Content-Disposition"])
    # unquoting turns to `attachment; filename=test_audio.wav`
    # use regex to get stuff past first `filename=` match (positive lookbehind)
    disposition_re = re.compile(r"(?<= filename\=).+")
    file_name = disposition_re.search(dec_disposition).group(0)

    # mime subtype
    file_mst = file_req_info["Content-Type"]
    logger.debug(
        f"{file_name}: {file_req_info['Content-Length']}b, {file_mst} hdr mime"
    )

    file_dat = file_req.read()

    assert conv_mime_daccodec(file_mst) == get_daccodec_from_buf(file_dat)

    return DACAudio(conv_mime_daccodec(file_mst), file_dat)
