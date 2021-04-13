""" Created by GigX Studio """

from Audio import Audio
import HotmoClient
import json

class AudioList:
    label = ''
    music = []

    def __init__(self, label):
        self.label = label

    def addAudio(self, data, duration):
        try:
            audioJSON = json.loads(data)
            artist = audioJSON['artist']
            title = audioJSON['title']
            url = audioJSON['url']
            id = audioJSON['id']
            img = HotmoClient.HOST + audioJSON['img']
            self.music.append(Audio(id, url, title, artist, img, duration))
        except:
            pass
        pass

    def getLabel(self):
        return self.label

    def getMusicList(self):
        return self.music

    def clearMusicList(self):
        self.music.clear()
        self.music = None
        pass
