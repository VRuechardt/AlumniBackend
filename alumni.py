from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from util.mail_service import mail

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='find.my.alumnis@gmail.com',
    MAIL_PASSWORD='7p3xX9!4-o',
    MAIL_DEFAULT_SENDER=('Alumni', 'find.my.alumnis@gmail.com'))


mail.init_app(app)

class HelloWorld(Resource):
    def get(self):
        #util.mail_service.send_registration_confirmation("valentin@ruechardt.de")

        return {'hello': 'world'}
    def post(self):
        return {'hello': 'vau'}


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

print __name__

if __name__ == '__main__':
    app.run()
