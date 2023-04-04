import requests
from recaptcha.captcha import Solve_Captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from PIL import Image
import img2pdf
import requests
from bs4 import BeautifulSoup
import time

captcha = Solve_Captcha()

fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
driver = webdriver.Firefox(firefox_profile=fp)
driver.get('https://esaj.tjsp.jus.br/sco/abrirCadastro.do')
time.sleep(2)
uuidcaptcha = driver.find_element(By.ID,'uuidCaptcha').get_attribute('value')
id_recaptcha = driver.find_element(By.ID,'id_recaptcha_response_token').get_attribute('value')
jsessionid = driver.get_cookies()[0]['value']
kjsessionis = driver.get_cookies()[1]['value']
utma = driver.get_cookies()[2]['value']
utmc = driver.get_cookies()[3]['value']
utmz = driver.get_cookies()[4]['value']
utmt = driver.get_cookies()[5]['value']
utmb = driver.get_cookies()[6]['value']



url = "https://esaj.tjsp.jus.br/sco/salvarCadastro.do"

payload='pedidoIntranet=false&entity.cdModelo=6&entity.tpPessoa=F&entity.tpPessoa=F&entity.nmPesquisa=Wesley Silva Cabral de Oliveira&entity.nuCpfFormatado=403.154.468-54&entity.nuRgFormatado=487882398&entity.nuRgDig=&entity.flGenero=M&entity.nmMae=Juliene Maria da Silva&entity.nmPai=&entity.dtNascimento=14%2F11%2F1992&entity.naturalidade.cdMunicipio=&entity.naturalidade.nmMunicipio=&entity.naturalidade.cdUf=&recaptcha_response_token={}&uuidCaptcha={}&entity.solicitante.deEmail=wesley.silva.cabral%40hotmail.com&confirmacaoInformacoes=true'.format(id_recaptcha,uuidcaptcha)
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': f'JSESSIONID={jsessionid}; K-JSESSIONID-bocbpjmm={kjsessionis}; __utmz={utmz}; __utma={utma}; __utmc={utmc}; __utmt={utmt}; __utmb={utmb}',
  'Origin': 'https://esaj.tjsp.jus.br',
  'Referer': 'https://esaj.tjsp.jus.br/sco/abrirCadastro.do',
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












with open('arquivo.html', 'w') as f:
    f.write(response.text)
fp = webdriver.FirefoxProfile()
fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
driver = webdriver.Firefox(firefox_profile=fp)
driver.get('file:///opt/projetos/original/certidoes/arquivo.html')
driver.get_full_page_screenshot_as_file('teste.png')
img_path = 'teste.png'
        
# storing pdf path
pdf_path = 'teste.png'.replace('png','pdf')

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