import os
import sys

from youtube2mp3.audio_dl import YoutubeAudioDL
from youtube2mp3.mp3 import save_as_mp3


def main():
    urls = sys.argv[1:]
    with YoutubeAudioDL() as dl:
        dl.download(urls)
        for file_name in dl.file_names:
            save_as_mp3(file_name)
            os.unlink(file_name)


if __name__ == "__main__":
    main()
