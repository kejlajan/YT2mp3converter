import os

from moviepy.editor import AudioFileClip


def save_as_mp3(file_name, clip_info):
    clip = AudioFileClip(file_name)
    if 'start' in clip_info or 'stop' in clip_info:
        start = clip_info.get('start', 0)
        stop = clip_info.get('stop', None)
        import pdb; pdb.set_trace()
        clip = clip.subclip(start, stop)
    name, suffix = os.path.splitext(file_name)
    clip.write_audiofile('{}.mp3'.format(name))
