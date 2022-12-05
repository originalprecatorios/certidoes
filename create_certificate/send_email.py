import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from email.mime.application import MIMEApplication

class Email:
    def __init_(self, login, pwd,attach, to = [], config = {}):
        self._attach = attach
        self._to = to
        self._config = config
        self._login = login
        self._pwd = pwd

    def send_email_ruralservice(self):
        address = self._config['user']
        passwd = self._config['passwd']
        receiver = self._to
        mail_content = """
            Segue pdf com os dados para solicitação de certidão
        """
        message = MIMEMultipart()
        message['From'] = address
        message['To'] = ", ".join(receiver)
        message['Subject'] = "Solicitação de Certidão"
        message.attach(MIMEText(mail_content))

        # Anexando o PDF
        pdfname=self._attach
        fp=open(pdfname,'rb')
        anexo = MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        anexo.add_header('Content-Disposition','attachment',filename=pdfname)
        message.attach(anexo)

        server = smtplib.SMTP('smtp.office365.com',587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self._login, self._pwd)
        text = message.as_string()
        server.sendmail(address, receiver, text)
        server.quit()
        print('Email enviado')