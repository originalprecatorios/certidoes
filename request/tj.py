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

class Tj():
    def __init__(self,pData):
        print('Tj')
        self.timeout_seconds = 10
        self._data = pData
        self._pasta = '/tmp/pdf/tj/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')

    def get_download(self):

        url = "https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta={}&cdForo=-1".format(self._data['cpf'])

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://esaj.tjsp.jus.br/cpopg/search.do;jsessionid=3679AEF0B3BEA3C1422C5432ACF3372C.cpopg7?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta={}&cdForo=-1'.format(self._data['cpf'].replace('.','').replace('-','')),
        'Cookie': 'JSESSIONID=E8CB374DA3F0C2AA36FF5163B49BFF35.cpopg7; K-JSESSIONID-knbbofpc=1BD91FB0B2263B20B5BDBEE65454FEC4; JSESSIONID=6E93CAA4BD4FED93FC70A5DC53E3AD3A.cpopg7; K-JSESSIONID-knbbofpc=1BD91FB0B2263B20B5BDBEE65454FEC4',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        print(response.text)


        with open(self._pasta+'{}.pdf'.format(self._data['cpf'].replace('.','').replace('-','')), 'wb') as f:
            f.write(response.content)
        
        print('Download concluido')