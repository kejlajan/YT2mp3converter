import os

import fire

from youtube2mp3.audio_dl import YoutubeAudioDL
from youtube2mp3.mp3 import save_as_mp3


def batch_download(*urls):
    with YoutubeAudioDL() as dl:
        dl.download(urls)
        for file_name in dl.file_names:
            save_as_mp3(file_name)
            os.unlink(file_name)


def get_clip(url, start, stop):
    pass


def main():
    fire.fire({
        'batch': batch_download,
        'clip': get_clip
        })


if __name__ == "__main__":
    main()
