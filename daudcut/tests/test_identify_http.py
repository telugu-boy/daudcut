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

from daudcut import dacaudio

if __name__ == "__main__":
    # wav
    assert (
        dacaudio.http_get_audio(
            "https://cdn.discordapp.com/attachments/827431844853055529/828484426525966367/test_audio.wav"
        ).codec.name
        == "WAVE"
    )
    # mp3
    assert (
        dacaudio.http_get_audio(
            "https://cdn.discordapp.com/attachments/827431844853055529/828474634730602566/test_audio.mp3"
        ).codec.name
        == "MP3"
    )
    # ogg (vorbis/opus)
    assert (
        dacaudio.http_get_audio(
            "https://cdn.discordapp.com/attachments/827431844853055529/828501784753733662/test_audio.ogg"
        ).codec.name
        == "VORBIS"
    )
