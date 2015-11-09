from flask_mail import Mail, Message

mail = Mail()


def send_registration_confirmation(email):

    msg = Message('Invitation from alumni network',
                  recipients=[email])
    msg.body = 'You were invited at find.my.alumnis. Congratulations!'

    mail.send(msg)

    print 'sent'
