import requests
from recaptcha.captcha import Solve_Captcha
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from PIL import Image
import img2pdf
import requests
import json

captcha = Solve_Captcha()
response = captcha.recaptcha('6LdBDtkUAAAAAPWtjfRT93OAzGSZojdvLA22RkNK','https://pje.trt2.jus.br/pje-certidoes-api/api/certidoes/trabalhistas/emissao')
url = "https://pje.trt2.jus.br/pje-certidoes-api/api/certidoes/trabalhistas/emissao"

payload = json.dumps({
  "criterioDeEmissao": "CPF",
  "nome": "",
  "numeroDoDocumento": "403.154.468-54",
  "respostaDoCaptcha": "{}".format(response)
})
headers = {
  'authority': 'pje.trt2.jus.br',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/json',
  'cookie': '_ga=GA1.3.371081492.1678111699',
  'origin': 'https://pje.trt2.jus.br',
  'referer': 'https://pje.trt2.jus.br/certidoes/trabalhista/emissao',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

url = "https://pje.trt2.jus.br/pje-certidoes-api/api/certidoes/trabalhistas/{}".format(response.text.split(':')[1].replace('}',''))

payload={}
headers = {
  'authority': 'pje.trt2.jus.br',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': '_ga=GA1.3.371081492.1678111699',
  'referer': 'https://pje.trt2.jus.br/certidoes/trabalhista/certidao/8189745320',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

texto_formatado = response.text.replace('src="assets/imagens/brasao.png\"','src="/opt/projetos/original/certidoes/templates/brasao.png"')
with open('/opt/projetos/original/certidoes/templates/response_css.text') as arquivo:
  dado = arquivo.read()
with open('arquivo.html', 'w') as f:
    f.write(texto_formatado)
    f.write(f'<style>{dado}</style>')
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