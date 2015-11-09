from flask import Flask, send_from_directory
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


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()

        print args

        return 201


class PutUser(Resource):
    def post(self):
        return 201
        #parser = reqparse.RequestParser()
        #parser.add_argument('email')
        #args = parser.parse_args()
        #task = {'task': args['mail']}
        #print(task)
        #return 201

api.add_resource(HelloWorld, '/api/')
api.add_resource(PutUser, '/api/putuser')
api.add_resource(Login, '/api/login')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def server_static(path):
    print '../Alumni/app/', path
    return send_from_directory('../Alumni/app/', path)


print __name__

if __name__ == '__main__':
    app.run()
