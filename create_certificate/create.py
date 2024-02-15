#!/usr/bin/python3
from jinja2 import Environment, FileSystemLoader
from pdfkit.api import configuration
from weasyprint import HTML
from datetime import datetime
from random import randint
import webbrowser, os, string, random
import shutil, json
from create_certificate.send_email import Email_enviar
from decouple import config

class Creat:

    def __init__(self,pData,pError):
        self._error = pError
        month_name = {
            '1': 'Janeiro',
            '2': 'Fevereiro',
            '3': 'Março',
            '4': 'Abril',
            '5': 'Maio',
            '6': 'Junho',
            '7': 'Julho',
            '8': 'Agosto',
            '9': 'Setembro',
            '10': 'Outubro',
            '11': 'Novembro',
            '12': 'Dezembro'        
        }
        self._data = pData
        estado = 'São Paulo'
        now = datetime.now()
        day = str(now.day)
        year = str(now.year)
        month = month_name[str(now.month)]
        self._dt = estado+', '+day+' de '+month+' de '+year

    def cert(self):
        try:
            print("função cert")
            path = os.path.abspath('')
            path_templates = os.path.join(path, 'templates/')
            path_images = os.path.join(path, 'imgs/')
            path_temp = os.path.join('/tmp',''.join(random.choices(string.ascii_uppercase + string.digits, k = 4)) + '/') #Pasta onde as imagens serão gravadas
            path_out = '/tmp/out/'

            # make temp dir
            os.makedirs(path_temp)
            try:
                shutil.rmtree(path_out)
            except:
                pass
            try:
                os.makedirs(path_out)
            except:
                pass

            env = Environment(loader=FileSystemLoader(path_templates))
            template = env.get_template("original.html")

            # variables for template

            template_vars = {"title":"Teste", "conteudo": "valores", 
                            "imgs_folder": path_images,
                            "grafico": "", 
                            "name": self._data['nome'], 
                            "name_mom": self._data['mae'], 
                            "rg": self._data['rg'], 
                            "cpf": self._data['cpf'][:-3],
                            "cpf_digit": self._data['cpf'].replace('.','').replace('-','')[-2:],
                            "org" : self._data['orgao_exp'],
                            "data" : self._dt
                            }

            html_out = template.render(template_vars)

            file_name = f"{path_out}certidao.pdf"
            #HTML(string=html_out).write_pdf(file_name, stylesheets=[f"{path_templates}styles.css"])
            HTML(string=html_out).write_pdf(file_name, stylesheets=[f"{path_templates}styles.css"])


            # remove temp path
            print("removendo pasta")
            shutil.rmtree(path_temp)


            smtp_config = {'host': os.environ['SMTP_SERVE'], 'port': os.environ['SMTP_PORT'], 'user': os.environ['SMTP_USER'], 'passwd':os.environ['SMTP_PASS']}
            e = Email_enviar(os.environ['SMTP_USER'],'@#$WSDEqasw1!',file_name,['certidao2instancia@tjsp.jus.br',self._data['email']],smtp_config)
            #e = Email_enviar(os.environ['SMTP_USER'],os.environ['SMTP_PASS'],file_name,[self._data['email']],smtp_config)
            texto = """
                        Segue pdf com os dados para solicitação de certificado
                    """
            e.send_email_ruralservice(path_out,texto)
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'estadual',
                    'funcao' : 'erro na função login',
                    'erro': e
            }
            self._error.addData(err)
            print(e)
            return