import os
import sys

from urllib.parse import urlparse

from youtube2mp3.audio_dl import YoutubeAudioDL
from youtube2mp3.mp3 import save_as_mp3


URL = "https://www.youtube.com/watch?v="


def main():
    urls = sys.argv[1:]
    with YoutubeAudioDL() as dl:
        clip_info_list = []
        cleansed_url = []
        for url in urls:
            result = urlparse(url)
            query, number = _get_query(result.query)
            cleansed_url.append(URL + query['v'])
            clip_info_list.append(query)
        dl.download(urls)
        for file_name, clip_info in zip(dl.file_names, clip_info_list):
            save_as_mp3(file_name, clip_info)
            os.unlink(file_name)


def _get_query(query):
    tokens = query.split('&')
    abc = {}
    number_of_keys = 0
    for token in tokens:
        key, value = token.split('=')
        abc[key] = value
        number_of_keys += 1
    return abc, number_of_keys


if __name__ == "__main__":
    main()
