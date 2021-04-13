""" Created by GigX Studio """

class Audio:
    id = ''
    url = ''
    title = ''
    artist = ''
    img = ''
    duration = ''

    def __init__(self, id, url, title, artist, img, duration):
        self.id = id.replace('track-id-', '')
        self.url = url
        self.title = title
        self.artist = artist
        if not 'no-cover' in img:
            self.img = img
        self.duration = duration

    def getId(self):
        return self.id

    def getUrl(self):
        return self.url

    def getTitle(self):
        return self.title

    def getArtist(self):
        return self.artist

    def getImg(self):
        return self.img

    def getDuration(self):
        return self.duration

    def toJSON(self):
        return '{\"id\":\"' + self.id + '\",\"title\":\"' + self.title + '\",\"artist\":\"' + self.artist + '\",\"img\":\"' + self.img + '\",\"url\":\"' + self.url + '\",\"duration\":\"' + self.duration + '\"}'