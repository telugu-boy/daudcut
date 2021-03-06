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

import sys
import logging

import dacaudio

if __name__ == "__main__":
    root = logging.getLogger("daudcut")
    root.setLevel(logging.DEBUG)

    stdouthandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stdouthandler.setFormatter(formatter)
    root.addHandler(stdouthandler)

    aud = dacaudio.http_get_audio(
        "https://cdn.discordapp.com/attachments/827431844853055529/828484426525966367/test_audio.wav"
    )
    print(aud.codec.name)
