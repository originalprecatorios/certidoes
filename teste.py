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


sitekey = '4a65992d-58fc-4812-8b87-789f7e7c4c4b'
captcha = Solve_Captcha()
r = captcha.resolve_hcaptcha(sitekey,'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')

url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Verificar"

payload=f'NI=289.336.228-10&h-captcha-response={r}'
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'ASP.NET_SessionId=0v2vx102maa4hqaq4i45mxcf; BIGipServerPOOL_SERVICO_RECEITA=1558680737.47873.0000',
  'Origin': 'https://solucoes.receita.fazenda.gov.br',
  'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni=28933622810"

payload={}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Cookie': 'ASP.NET_SessionId=0v2vx102maa4hqaq4i45mxcf; BIGipServerPOOL_SERVICO_RECEITA=1558680737.47873.0000',
  'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Verificar',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/Emitir?Ni=28933622810"

payload={}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Cookie': 'ASP.NET_SessionId=0v2vx102maa4hqaq4i45mxcf; BIGipServerPOOL_SERVICO_RECEITA=1558680737.47873.0000',
  'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni=28933622810',
  'Sec-Fetch-Dest': 'iframe',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

pasta = '/tmp/pdf/'
if os.path.isdir(f'{pasta}'):
    print("O diretório existe!")
else:
    os.makedirs(f'{pasta}')

headers

fp = webdriver.FirefoxProfile()

fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", pasta)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                  "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
fp.set_preference("pdfjs.disabled", True)
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_profile=fp)
driver.get('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni=28933622810')
time.sleep(2)



url = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/ResultadoEmissao/NDUkODk3OCMyMzQ2Nzg5IyojKjAwNjUsbyBDUEYsMjg5LjMzNi4yMjgtMTA="

payload={}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Cookie': 'ASP.NET_SessionId=0v2vx102maa4hqaq4i45mxcf; BIGipServerPOOL_SERVICO_RECEITA=1558680737.47873.0000',
  'Referer': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni=28933622810',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)