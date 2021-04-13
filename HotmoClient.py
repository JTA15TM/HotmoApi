""" Created by GigX Studio """

import requests
from Audio import Audio
from AudioList import AudioList
from Genre import Genre
from RequestResult import RequestResult

HOST = 'https://ruv.hotmo.org'
MAIN = 1
SEARCH = 2
GENRE = 3
GENRE_LIST = 4

def hotmoMain():
    mdata = requests.get(HOST)
    if mdata.status_code == 200:
        mdat = hotmoParseList(mdata.text, MAIN)
        return RequestResult(True, mdat, MAIN)
    else:
        return RequestResult(False, None, MAIN)
    pass

def hotmoSearch(q='Marshmello'):
    if len(q) > 0:
        sdata = requests.get(HOST + '/search?q=' + q)
        if sdata.status_code == 200:
            sdat = hotmoParseList(sdata.text, SEARCH)
            return RequestResult(True, sdat, SEARCH)
    return RequestResult(False, None, SEARCH)

def hotmoGenre(genre=1):
    gdata = requests.get(HOST + '/genre/' + str(genre))
    if gdata.status_code == 200:
        gdat = hotmoParseList(gdata.text, GENRE)
        return RequestResult(True, gdat, GENRE)
    else:
        return RequestResult(False, None, GENRE)
    pass

def hotmoGenresList():
    gldata = requests.get(HOST + '/genres')
    if gldata.status_code == 200:
        gldat = hotmoGenresListParse(gldata.text)
        return RequestResult(True, gldat, GENRE_LIST)
    else:
        return RequestResult(False, None, GENRE_LIST)
    pass

def hotmoGenresListParse(data):
    genres = []

    audioListTagElement = 'class="album-list">'
    audioListCloseTagElement = '</ul>'
    if (audioListTagElement in data) and (audioListCloseTagElement in data):
        audioListStart = data.find(audioListTagElement) + len(audioListTagElement)
        audioListEnd = data.find(audioListCloseTagElement, audioListStart)
        if audioListEnd > audioListStart:
            albumList = data[audioListStart:audioListEnd]
            genreDivs = albumList.split('<a href="/genre/')
            for index in range(len(genreDivs)):
                genreDiv = genreDivs[index]
                codeTag = '\">'
                if codeTag in genreDiv and '</a>' in genreDiv:
                    codeDivEnd = genreDiv.find(codeTag)
                    if codeDivEnd > -1:
                        codeStr = genreDiv[:codeDivEnd]
                        if '" class="album-link' in codeStr:
                            codeStr = codeStr.replace('" class="album-link', '')
                            codeStr = codeStr.strip()
                        code = -1
                        label = ''
                        img = ''
                        try:
                            code = int(codeStr)
                        except:
                            code = -1

                        labelOpenTagElement = 'class="album-title">'
                        labelCloseTagElement = '</span>'
                        if labelOpenTagElement in genreDiv and labelCloseTagElement in genreDiv:
                            labelStart = genreDiv.find(labelOpenTagElement) + len(labelOpenTagElement)
                            labelEnd = genreDiv.find(labelCloseTagElement, labelStart)
                            if (labelStart > -1) and (labelEnd > labelStart):
                                label = genreDiv[labelStart:labelEnd]

                        imgOpenTagElement = 'class="album-image"'
                        imgCloseTagElement = '\')'
                        if imgOpenTagElement in genreDiv and imgCloseTagElement in genreDiv:
                            imgStart = genreDiv.find(imgOpenTagElement) + len(imgOpenTagElement)
                            imgEnd = genreDiv.find(imgCloseTagElement, imgStart)
                            if (labelStart > -1) and (labelEnd > labelStart):
                                imgElement = genreDiv[imgStart:imgEnd]
                                imgl_tag_start = 'url(\''
                                imgl_start = imgElement.find(imgl_tag_start) + len(imgl_tag_start)
                                img = 'https:' + imgElement[imgl_start:]

                        genres.append(Genre(label, code, img))
    return genres

def hotmoParseList(data, code):
    label_tag_element = ''
    if code == MAIN:
        label_tag_element = '<h2 class="tracks__title content-item-title">'
    elif code == GENRE:
        label_tag_element = '<h1 class="p-info-title">'

    blocks = data.split('<div class="content-item tracks">')
    musicBlocks = []
    for index in range(len(blocks)):
        block = blocks[index]
        if label_tag_element in block:
            musicBlocks.append(block)

    outputList = []

    for a in range(len(musicBlocks)):
        musicBlock = musicBlocks[a]
        if 'tracks__list' in musicBlock:
            list = musicBlock.split('data-musmeta=')

            label = ''
            if code == MAIN or code == GENRE:
                if label_tag_element in musicBlock:
                    labelStart = musicBlock.find(label_tag_element)

                    h_close_tag = '</h'
                    if code == MAIN:
                        h_close_tag = h_close_tag + '2>'
                    elif code == GENRE:
                        h_close_tag = h_close_tag + '1>'
                    labelEnd = musicBlock.find(h_close_tag)
                    if labelStart > -1 and (labelEnd > -1 and labelEnd > labelStart):
                        label = musicBlock[labelStart + len(label_tag_element):labelEnd].strip()
            elif code == SEARCH:
                label = 'Результаты поиска'

            audioList = AudioList(label)
            for b in range(len(list)):
                musmeta = list[b]

                duration_tag_element = '<div class="track__fulltime">'
                duration_tag_close = '</div>'
                duration = ''
                if duration_tag_element in musmeta:
                    durationStart = musmeta.find(duration_tag_element)
                    if durationStart > -1:
                        duration = musmeta[durationStart + len(duration_tag_element):]
                        if duration_tag_close in duration:
                            durationEnd = duration.find(duration_tag_close)
                            if durationEnd > -1:
                                duration = duration[:durationEnd]

                startJSON = musmeta.find('{')
                endJSON = musmeta.find('}')
                if startJSON > -1 and (endJSON > -1 and endJSON > startJSON):
                    audioList.addAudio(musmeta[startJSON:endJSON + 1], duration)
            if code == MAIN:
                outputList.append(audioList)
            elif code == SEARCH or code == GENRE:
                return audioList
    if code == MAIN:
        return outputList
    return AudioList('Нет аудиозаписей')