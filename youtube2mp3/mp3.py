import os
from datetime import datetime

from moviepy.editor import AudioFileClip


TIME_FORMAT = '%H:%M:%S'


def save_as_mp3(file_name, clip_info):
    clip = AudioFileClip(file_name)
    t_start, t_end = parse_clip_info(clip_info)
    clip = clip.subclip(t_start=t_start, t_end=t_end)
    name, suffix = os.path.splitext(file_name)
    try:
        clip.write_audiofile('{}.mp3'.format(name))
    except IndexError:
        print("Please try a bit longer duration")
        raise


def parse_clip_info(clip_info):
    t_start = 0
    t_end = None
    if 'start' in clip_info or 'stop' in clip_info:
        start = clip_info.get('start', 0)
        stop = clip_info.get('stop', None)

        if start:
            start = get_time(start)
            t_start = (start.hour, start.minute, start.second)
            if stop:
                stop = get_time(stop)
                duration = stop - start
                t_end = duration.total_seconds()
        else:
            stop = get_time(stop)
            t_end = stop.total_seconds()
    return t_start, t_end


def get_time(time_string):
    return datetime.strptime(time_string, TIME_FORMAT)
