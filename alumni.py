from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from decorators import crossorigin

app = Flask(__name__)
CORS(app)
api = Api(app)


class HelloWorld(Resource):
    def post(self):
        return {'hello': 'world'}

class PutUser(Resource):
    def post(self):
        return 201
        #parser = reqparse.RequestParser()
        #parser.add_argument('email')
        #args = parser.parse_args()
        #task = {'task': args['mail']}
        #print(task)
        #return 201

api.add_resource(HelloWorld, '/')
api.add_resource(PutUser, '/PutUser')

if __name__ == '__main__':
    app.run()
