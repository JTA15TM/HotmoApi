""" Api, when search music in hotmo.org """
""" Created by GigX Studio """

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import request
import random
app = Flask(__name__)
api = Api(app)

import HotmoClient
from HotmoClient import *
from Audio import Audio
from Genre import Genre
from HotmoJSON import *
from RequestResult import RequestResult

class HotmoRequests(Resource):
    def get(self, id=0):
        args = request.args

        if 'get' in args:
            method = args['get']

            if 'main' in method:
                mresult = hotmoMain()
                if mresult.isSuccess():
                    return audioListstoJSON(mresult.getData())
                else:
                    return '{"error":"Server connection error"}'

            elif 'genre' in method and 'id' in args:
                id = args['id']
                gresult = hotmoGenre(genre=id)
                if gresult.isSuccess():
                    return audioListToJSON(gresult.getData())
                else:
                    return '{"error":"Server connection error"}'

            elif 'search' in method and 'q' in args:
                q = args['q']
                sresult = hotmoSearch(q=str(q))
                if sresult.isSuccess():
                    return audioListToJSON(sresult.getData())
                else:
                    return '{"error":"Server connection error"}'

            elif 'genreList' in method:
                glresult = hotmoGenresList()
                if glresult.isSuccess():
                    return genresToJSON(glresult.getData())
                else:
                    return '{"error":"Server connection error"}'


        return '{"error":"unknown method called"}'

api.add_resource(HotmoRequests, "/method")
if __name__ == '__main__':
    app.run(debug=True)