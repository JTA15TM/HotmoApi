""" Created by GigX Studio """

class Genre:
    label = ''
    img = ''
    id = -1

    def __init__(self, label, id, img):
        self.label = label
        self.img = img
        self.id = id

    def getId(self):
        return self.id

    def getLabel(self):
        return self.label

    def getImg(self):
        return self.img

    def toJson(self):
        return '{\"label\":\"' + self.label + '\", \"id\":' + str(self.id) + ', \"img\":\"' + self.img + '\"}'