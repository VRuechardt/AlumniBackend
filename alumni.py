from flask import Flask, send_from_directory, session
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from util.mail_service import mail
from endpoints import user

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


api.add_resource(user.User, '/api/user')
api.add_resource(user.Login, '/api/login')
api.add_resource(user.Logout, '/api/logout')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def server_static(path):
    print '../Alumni/app/', path
    return send_from_directory('../Alumni/app/', path)

app.secret_key = '7p3xX9!4-o'


print __name__

if __name__ == '__main__':
    app.run()
