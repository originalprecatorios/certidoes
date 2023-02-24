import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os, time, shutil
from email.mime.application import MIMEApplication

class Email_enviar:
    def __init__(self, login, pwd,attach, to = [], config = {}):
        print("Email_enviar")
        self._attach = attach
        self._to = to
        self._config = config
        self._login = login
        self._pwd = pwd

    def send_email_ruralservice(self,path_temp):
        try:
            print("send_email_ruralservice")
            address = self._config['user']
            passwd = self._config['passwd']
            receiver = self._to
            mail_content = """
                Segue pdf com os dados para solicitação de certificado
            """
            message = MIMEMultipart()
            message['From'] = address
            message['To'] = ", ".join(receiver)
            message['Subject'] = "Solicitação de Certidão"
            message.attach(MIMEText(mail_content))
            print(message)
            # Anexando o PDF
            pdfname=self._attach
            fp=open(pdfname,'rb')
            anexo = MIMEApplication(fp.read(),_subtype="pdf")
            fp.close()
            anexo.add_header('Content-Disposition','attachment',filename='certidao.pdf')
            message.attach(anexo)
            print('pdf anexado')
            server = smtplib.SMTP('smtp.office365.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            print(self._login, self._pwd)
            server.login(self._login, self._pwd)
            print('server login')
            text = message.as_string()
            server.sendmail(address, receiver, text)
            server.quit()
            print('Email enviado')
            time.sleep(2)
            try:
                os.remove(path_temp+'certidao.pdf')
            except:
                pass
        except Exception as e:
            print(e)