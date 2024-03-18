import requests
from recaptcha.captcha import Solve_Captcha
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
from recaptcha.captcha import Solve_Captcha
import undetected_chromedriver as uc

class Federal_request():
    def __init__(self,pCnpj):
        print('Federal_request')
        self.timeout_seconds = 10
        self._sitekey = '4a65992d-58fc-4812-8b87-789f7e7c4c4b'
        self._captcha = Solve_Captcha()
        self._r = self._captcha.resolve_hcaptcha(self._sitekey,'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')
        self._cnpj = pCnpj

    def get_cookies(self):
        url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Verificar"

        payload='NI={}&h-captcha-response={}'.format(self._cnpj,self._r)
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://solucoes.receita.fazenda.gov.br',
        'Connection': 'keep-alive',
        'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir',
        'Cookie': 'BIGipServerPOOL_SERVICO_RECEITA=1541903521.47873.0000; ASP.NET_SessionId=faozoqgfai2fsoi1hgxkral1; fileDownload=true',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        print(response.text)


        url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni={}".format(self._cnpj.replace('.','').replace('-',''))

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Verificar',
        'Cookie': 'BIGipServerPOOL_SERVICO_RECEITA=1541903521.47873.0000; ASP.NET_SessionId=faozoqgfai2fsoi1hgxkral1; fileDownload=true',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        print(response.text)

        
        url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Emitir?Ni={}".format(self._cnpj.replace('.','').replace('-',''))

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni={}'.format(self._cnpj.replace('.','').replace('-','')),
        'Cookie': 'BIGipServerPOOL_SERVICO_RECEITA=1541903521.47873.0000; ASP.NET_SessionId=faozoqgfai2fsoi1hgxkral1; fileDownload=true',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin'
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=self.timeout_seconds)

        print(response.text)

        return response