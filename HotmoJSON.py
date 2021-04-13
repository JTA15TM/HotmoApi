""" Created by GigX Studio """

from Genre import Genre
from AudioList import *

def genresToJSON(data):
    output = '{\"items\":['
    size = len(data)
    for index in range(size):
            genre = data[index]
            output = output + genre.toJson()
            if index < size - 1:
                output = output + ','
            
    output = output + ']}'
    return output

def audiosToJSON(data):
    output = '\"audios\":['
    size = len(data)
    for index in range(size):
            audio = data[index]
            output = output + audio.toJSON()
            if index < size - 1:
                output = output + ','
            
    output = output + ']'
    return output

def audioListToJSON(data):
    output = '{\"label\":\"' + data.getLabel() + '\", ' + audiosToJSON(data.getMusicList()) + '}'
    data.clearMusicList()
    return output

def audioListstoJSON(data):
    output = '{\"lists\":['
    size = len(data)
    for index in range(size):
            audioList = data[index]
            output = output + audioListToJSON(audioList)
            if index < size - 1:
                output = output + ','
    return output + ']}'