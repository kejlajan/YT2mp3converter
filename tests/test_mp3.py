from mock import patch
from nose.tools import eq_
from youtube2mp3.mp3 import parse_clip_info, save_as_mp3


def test_parse_clip_info():
    t_start, t_end = parse_clip_info({
        "start": "00:00:11",
        "stop": "00:00:22"
        })
    eq_((0, 0, 11), t_start)
    eq_(11, t_end)


@patch("youtube2mp3.mp3.AudioFileClip")
def test_webm(mocked_audio_file_clip):
    save_as_mp3('afile', {
        "start": "00:01:00",
        "stop": "00:02:00"
    })
