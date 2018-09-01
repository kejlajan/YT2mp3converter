from youtube_dl import YoutubeDL


OPTIONS = {
    'extractaudio': True,
    'format': 'bestaudio/best',
    'postprocessors': []
}


class YoutubeAudioDL(YoutubeDL):

    def __init__(self):
        super(YoutubeAudioDL, self).__init__(OPTIONS)
        self.file_names = []

    def post_process(self, filename, ie_info):
        self.file_names.append(filename)
        super(YoutubeAudioDL, self).post_process(filename, ie_info)
