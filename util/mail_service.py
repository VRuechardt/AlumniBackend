from flask_mail import Mail, Message

mail = Mail()


def send_registration_confirmation(email, code):

    msg = Message('Invitation from alumni network',
                  recipients=[email])
    msg.html = 'You were invited at find.my.alumnis. Congratulations!<br><br>Please click on the following link to register<br><a href="http://localhost:5000/#/register/' + code + '">Link</a>'

    mail.send(msg)

    print 'sent'

