""" Created by GigX Studio """

class RequestResult:
    success = False
    data = None
    code = -1

    def __init__(self, success, data, code):
        self.success = success
        self.data = data
        self.code = code

    def getCode(self):
        return self.code

    def getData(self):
        return self.data

    def isSuccess(self):
        return self.success