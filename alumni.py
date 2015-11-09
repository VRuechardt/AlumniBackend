from flask import Flask
from flask_restful import Resource, Api
from flask.ext.cors import CORS
import util.mail_service
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

api.add_resource(HelloWorld, '/')

print __name__

if __name__ == '__main__':
    app.run()
