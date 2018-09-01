import os

from moviepy.editor import AudioFileClip


def save_as_mp3(file_name):
    clip = AudioFileClip(file_name)
    name, suffix = os.path.splitext(file_name)
    clip.write_audiofile('{}.mp3'.format(name))
