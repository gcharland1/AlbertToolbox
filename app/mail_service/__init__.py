import flask
import flask_mail

from app import mail


def reset_password(email, username, temp_link):
    try:
        subject = "Réinitialisation de votre mot de passe"
        msg_body = flask.render_template("mail_service/reset_password.html", username=username, link=temp_link)
        send_html_mail([email], subject, msg_body)
        return True
    except:
        return False

def send_html_mail(recipients, subject, body):
    msg = flask_mail.Message()
    msg.subject = subject
    msg.recipients = recipients
    msg.html = body
    print(type(mail))
    mail.send(msg)