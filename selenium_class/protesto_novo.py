from importlib.resources import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pathlib import Path
import time, os, shutil
import img2pdf
from PIL import Image
import undetected_chromedriver as uc
from decouple import config
from selenium.webdriver.common.action_chains import ActionChains
import base64
import json
import requests


class Protesto:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Robo Protesto')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')
        self._pasta = self._data['path']
        #self._pasta = '/opt/certidao/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
            
        
    
    def login(self,usr,pwd):
        try:
            url = "https://api.cenprotnacional.org.br/auth/login"
            formatado = usr.replace('.','').replace('-','')
            payload = f'{{"cpf":"{formatado}","senha":"{pwd}","tokenCaptcha":""}}'
            headers = {
            'authority': 'api.cenprotnacional.org.br',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.pesquisaprotesto.com.br',
            'referer': 'https://www.pesquisaprotesto.com.br/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            url = f"https://api.cenprotnacional.org.br/consulta/gerarComprovante/{self._data['cpf'].replace('.','').replace('-','')}/t/{json.loads(response.text)['token']}"

            payload = {}
            headers = {
            'authority': 'api.cenprotnacional.org.br',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://www.pesquisaprotesto.com.br',
            'referer': 'https://www.pesquisaprotesto.com.br/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }

            response = requests.request("GET", url, headers=headers, data=payload)     
            pdf_content_base64 = json.loads(response.text)["file"]
            pdf_content = base64.b64decode(pdf_content_base64)
            pdf_filename = f"{self._pasta}13- CENPROT.pdf"
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(pdf_content)
            
            for arquivo in os.listdir(self._pasta):
                if arquivo.find('13- CENPROT.pdf') > -1:
                    print('Download concluido para o cpf {}'.format(self._data['cpf']))
                    
                    return
            print('arquivo não foi gerado')
            self._driver.close()
    

        except Exception as e:
            self._driver.close()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "resultado-pesquisa"))).text
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            return

    def convert(self,pName):
        # storing image path
        img_path = pName
        
        # storing pdf path
        pdf_path = pName.replace('png','pdf')
        
        # opening image
        image = Image.open(img_path)
        
        # converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(image.filename)
        
        # opening or creating pdf file
        file = open(pdf_path, "wb")
        
        # writing pdf files with chunks
        file.write(pdf_bytes)
        
        # closing image file
        image.close()
        
        # closing pdf file
        file.close()
        
        os.remove(img_path)
        # output
        print("Successfully made pdf file")
    
    ########## looping até o download concluir 
    def _download(self):
        
        while True:
            cont = 0
            for arquivo in os.listdir(self._save):
                if arquivo.find('crdownload') > -1 and cont <= 6:
                    print('Aguardando término do download')
                    time.sleep(5)
                    cont += 1
                else:
                    return
            return