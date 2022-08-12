import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import time, os
import undetected_chromedriver as uc

class Divida_ativa():
    def __init__(self,pData,pCaptcha):
        print('Divida_ativa')
        self._data = pData
        self._sitekey = '6Le9EjMUAAAAAPKi-JVCzXgY_ePjRV9FFVLmWKB_'
        self._captcha = pCaptcha
        self._r = self._captcha.recaptcha(self._sitekey,'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf')
        self._pasta = '/tmp/pdf/divida_ativa/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')

    def get_download(self):
        url = "https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf"

        payload='emitirCrda=emitirCrda&emitirCrda%3AcrdaInputCnpjBase=&emitirCrda%3AcrdaInputCpf={}&g-recaptcha-response={}&emitirCrda%3Aj_id95=Emitir&javax.faces.ViewState=j_id2'.format(self._data['cpf'],self._r)
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.dividaativa.pge.sp.gov.br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf;jsessionid=524AA237088F50590D560C87068D972F.395016-sc-01',
        'Cookie': 'JSESSIONID=524AA237088F50590D560C87068D972F.395016-sc-01',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("POST", url, headers=headers, data=payload)


        with open(self._pasta+'{}.pdf'.format(self._data['cpf'].replace('.','').replace('-','')), 'wb') as f:
            f.write(response.content)
        
        print('Download concluido')