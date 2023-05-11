import smtplib, ssl
from email.message import EmailMessage
from decouple import config

class Smtp:

    def __init__(self):
        pass

    def _Envia_Email(self,to="junior.ppp@gmail.com",txtmsg="Teste"):
        msg = EmailMessage()
        msg.set_content(f"{txtmsg}")
        msg["Subject"] = "Email de notificação"
        msg["From"] = f"{config('SMTP_USER')}"
        msg["To"] = to

        context=ssl.create_default_context()

        with smtplib.SMTP(config('SMTP_SERVE'), port= config('SMTP_PORT')) as smtp:
            smtp.starttls(context=context)
            smtp.login(config('SMTP_USER'), config('SMTP_PASS'))
            smtp.send_message(msg)