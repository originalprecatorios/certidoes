import httpx
import os
import pdfkit
import time
from recaptcha.captcha import Solve_Captcha

cap = Solve_Captcha()
url = "https://www2.ssp.sp.gov.br/aacweb/carrega-formulario"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=0000MXy1891S8c64jGyH2HP7kbl:1eirm4393',
    'Referer': 'https://www2.ssp.sp.gov.br/aacweb/carrega-iframe',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}

# Criar uma instância do cliente HTTP
client = httpx.Client()

# Fazer a requisição usando o método GET
response = client.get(url, headers=headers)

# Verificar o status da resposta
if response.status_code == 200:
    
    sitekey = response.text.split('data-sitekey=')[1].split('\r')[0].replace('"','')
else:
    print(f"Erro {response.status_code} ao fazer a solicitação")

# Fechar a instância do cliente HTTP
client.close()
resposta = cap.recaptcha(sitekey,'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario')



url = "https://www2.ssp.sp.gov.br/aacweb/emitir-atestado.action"
payload = {
    "nome": 'WESLEY SILVA CABRAL DE OLIVEIRA',
    "numero": '48788239',
    "digito": '8',
    "txtDIAE": '26',
    "txtMESE": '03',
    "txtANOE": '2003',
    "sexo": 'M',
    "txtDIA": '14',
    "txtMES": '11',
    "txtANO": '1992',
    "nomePai": 'ANTONIO CABRAL DE OLIVEIRA',
    "nomeMae": 'JULIENE MARIA DA SILVA',
    "g-recaptcha-response": resposta,
    "pesquisa": "Pesquisar"
}
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded',
'Cookie': 'JSESSIONID=0000MXy1891S8c64jGyH2HP7kbl:1eirm4393',
'Origin': 'https://www2.ssp.sp.gov.br',
'Referer': 'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario',
'Sec-Fetch-Dest': 'iframe',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Linux"'
}

try:
    response = httpx.get(url, headers=headers, params=payload)
except:
    time.sleep(5)
    response = httpx.get(url, headers=headers, params=payload)

print(response.text)

pdf_file_path = '/opt/files/certidoes/wEz0uA9nM1QUgdV/ANTECEDENTES CRIMINAIS.pdf'
if response.headers.get("content-type") == "application/pdf":
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(response.content)
    print("Arquivo PDF salvo com sucesso.")
else:
    
    pdfkit.from_string(response.text.replace('/AACWEBSTATIC/img/imp_cab.gif','https://www2.ssp.sp.gov.br/AACWEBSTATIC/img/imp_cab.gif'), pdf_file_path, options={'encoding': 'utf-8'})
    time.sleep(5)
    print("Arquivo PDF salvo com sucesso.")

for arquivo in os.listdir('/opt/files/certidoes/wEz0uA9nM1QUgdV/'):
    if arquivo.find('ANTECEDENTES CRIMINAIS.pdf') > -1:
        print('Download do arquivo gerado para o cliente')