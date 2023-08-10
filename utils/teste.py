import requests
from recaptcha.captcha import Solve_Captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.firefox.options import Options 
from PIL import Image
import img2pdf
import requests
import pdfkit
import time
from utils.selenium_classes import Selenium_classes


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests

teste = Selenium_classes()
teste.firefox('https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao')
retorno = teste.wait_element("ID", "jurisdicao")


tempo_inicial = (time.time())
retorno = teste.element("ID", "jurisdicao")
tempo_final = (time.time())
print(f" teste1 {tempo_final - tempo_inicial} segundos")

tempo_inicial = (time.time())
retorno = teste.teste()
tempo_final = (time.time())
print(f"teste2 {tempo_final - tempo_inicial} segundos")
retorno1 = teste.wait_element("ID", "periodo-2").click()
retorno2 = teste.wait_element("NAME", "periodo", True)

url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao"

payload='tipoDocumentoPesquisado=1&numeroDocumentoPesquisado=403.154.468-54&nomePesquisado=WESLEY SILVA CABRAL DE OLIVEIRA&jurisdicao=0&periodo=1&data_inicial=&data_final=&captcha%5Bid%5D=094d3ded8b52b7985ca9f23f06884d13&captcha%5Binput%5D=pozir&submit=&submit='
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'PHPSESSID=u8tgdpegtsbo0mf29rohujef33; _ga=GA1.3.1642829368.1690392484; _gid=GA1.3.2048915482.1690392484; _gat=1; ww2.trtsp.jus.br={%22contraste%22:0%2C%22fontes%22:1%2C%22escalabilidade%22:0}; contraste=0; fontes=1; escalabilidade=0; PHPSESSID=gq1hsmk5poa9ag5gdeoesftup1',
  'Origin': 'https://aplicacoes10.trt2.jus.br',
  'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/recuperarcertidao"

payload={}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Cookie': 'PHPSESSID=u8tgdpegtsbo0mf29rohujef33; _ga=GA1.3.1642829368.1690392484; _gid=GA1.3.2048915482.1690392484; ww2.trtsp.jus.br={%22contraste%22:0%2C%22fontes%22:1%2C%22escalabilidade%22:0}; contraste=0; fontes=1; escalabilidade=0; _gat=1; PHPSESSID=gq1hsmk5poa9ag5gdeoesftup1',
  'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/imprimecertidao',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

if response.headers.get("content-type") == "application/pdf":
  with open('teste.pdf', "wb") as pdf_file:
      pdf_file.write(response.content)
  print("Arquivo PDF salvo com sucesso.")











captcha = Solve_Captcha()
response = captcha.recaptcha(sitekey,'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx')

url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Consulta.aspx"

#payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00864879873&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=CMW6H63&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00647072572&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=BSA5349&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(viewstate,viewstate_generator,event_validation,response)
#payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00833014943&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=DMX6834&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://www.ipva.fazenda.sp.gov.br',
  'Connection': 'keep-alive',
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
  'Cookie': cookies,
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Pages/Aviso.aspx"

payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
  'Connection': 'keep-alive',
  'Cookie': cookies,
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

# Conteúdo HTML da resposta
html_content = response.text

# Caminho e nome do arquivo PDF que você deseja criar
pdf_file_path = 'resultado.pdf'

# Defina a codificação do texto HTML (por exemplo, UTF-8)
html_encoding = 'utf-8'

# Crie o arquivo PDF a partir do conteúdo HTML e especificando a codificação
pdfkit.from_string(html_content, pdf_file_path, options={'encoding': html_encoding})

print(f"Arquivo PDF salvo em: {pdf_file_path}")


















#fp = webdriver.FirefoxProfile()
options = Options()
#options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get('https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx')
time.sleep(2)
arr ={'NET_SessionId':driver.get_cookies()[0]['value'],
      'TS01308bf5':driver.get_cookies()[1]['value'],
      'ai_user':driver.get_cookies()[2]['value'],
      'ai_session':driver.get_cookies()[3]['value'],
      'viewstate_generator':driver.find_element(By.ID,'__VIEWSTATEGENERATOR').get_attribute('value').replace('/','%2F').replace('+','%2B').replace('=','%3D'),
      'event_validation':driver.find_element(By.ID,'__EVENTVALIDATION').get_attribute('value').replace('/','%2F').replace('+','%2B').replace('=','%3D'),
      'viewstate':driver.find_element(By.ID,'__VIEWSTATE').get_attribute('value').replace('/','%2F').replace('+','%2B').replace('=','%3D'),
}
sitekey = driver.find_element(By.ID,'conteudoPaginaPlaceHolder_g_recaptcha').get_attribute('data-sitekey')
driver.close()
cookies = '_ga_7RC6MLS8YN=GS1.1.1683597623.5.0.1683597631.0.0.0; _ga=GA1.1.825311961.1661543027;ASP.NET_SessionId={}; TS01308bf5={}; ai_user={}; ai_session={}'.format(arr['NET_SessionId'],arr['TS01308bf5'],arr['ai_user'],arr['ai_session'])     
'''url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': cookies,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}

# Fazer a requisição usando o método GET
response = requests.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    # Extrair os valores dos campos do cabeçalho da resposta
    soup = BeautifulSoup(response.text, "html.parser")
    viewstate_generator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"]
    event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]
    viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"]
    
    # Obter os cookies
    cookies = response.cookies
    
    # Imprimir os valores dos campos e os cookies
    print("__VIEWSTATEGENERATOR:", viewstate_generator)
    print("__EVENTVALIDATION:", event_validation)
    print("NET_SessionId:", cookies.get("ASP.NET_SessionId"))
    print("TS01308bf5:", cookies.get("TS01308bf5"))
    print("ai_session:", cookies.get("ai_session"))
    
else:
    print(f"Erro {response.status_code} ao fazer a solicitação")'''

captcha = Solve_Captcha()

#sitekey = response.text.split('data-sitekey=')[1].split('>')[0].replace('"','')

response = captcha.recaptcha(sitekey,'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx')

url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Consulta.aspx"

payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00864879873&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=CMW6H63&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
#payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00647072572&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=BSA5349&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
#payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00833014943&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=DMX6834&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://www.ipva.fazenda.sp.gov.br',
  'Connection': 'keep-alive',
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
  'Cookie': cookies,
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Pages/Aviso.aspx"

payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
  'Connection': 'keep-alive',
  'Cookie': cookies,
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


























url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx"

payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam=00833014943&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca=DMX6834&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(arr['viewstate'],arr['viewstate_generator'],arr['event_validation'],response)
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': cookies,
  'Origin': 'https://www.ipva.fazenda.sp.gov.br',
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Pages/Aviso.aspx"

payload={}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Cookie': cookies,
  'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)