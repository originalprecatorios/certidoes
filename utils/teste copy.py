import requests
from recaptcha.captcha import Solve_Captcha
import os
from PIL import Image
import pdfkit
import requests
import time
import io
import httpx
from weasyprint import HTML
import requests
import base64

def load_captcha():
    response = requests.get('https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=DOCPARTE&dadosConsulta.valorConsulta=40315446854&cdForo=-1')

    with open('teste.html','wb') as f:
        f.write(response.content)
    
    with open('teste.html','r') as f:
        html_contente = f.read()
    
    html_contente_modify = html_contente.replace('/cpopg/softheme/src/css/app.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/softheme/src/css/app.css?v=2.8.34-30').replace('/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/softheme/src/fonts/saj/styles.css?v=2.8.34-30').replace('/cpopg/css/formulario.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/css/formulario.css?v=2.8.34-30').replace('/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2.css?v=2.8.34-30').replace('/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30','https://esaj.tjsp.jus.br/cpopg/webjars/select2/3.5.4/select2-bootstrap.css?v=2.8.34-30').replace('/cpopg/css/saj/select2/saj-select2.css','https://esaj.tjsp.jus.br/cpopg/css/saj/select2/saj-select2.css')

    with open('teste.html','w', encoding='utf-8') as f:
        f.write(html_contente_modify)

    with open('teste.html', 'rb') as f:
        html_content = f.read()

    # Criar um objeto HTML
    html = HTML(string=html_content)

    # Salvar o arquivo PDF
    html.write_pdf('teste.pdf')

    JSESSIONID = response.cookies.get('JSESSIONID')


    response = requests.get('https://cndt-certidao.tst.jus.br/inicio.faces')
    viewstate = response.text.split('javax.faces.ViewState:0" value="')[1].split('"')[0]
    jd_id = 'j_id_jsp_'+response.text.split('name="j_id_jsp_')[1].split('"')[0]

    url = "https://cndt-certidao.tst.jus.br/api"

    payload={}
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID={}; 7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR;'.format(response.cookies.get_dict()['JSESSIONID'],response.cookies.get_dict()['7aa721eeaef392956e2c4add5997cdb0']),
    'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces;jsessionid={}'.format(response.cookies.get_dict()['JSESSIONID']),
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    token_desafio = data["tokenDesafio"]

    imagem_bytes = bytes((x & 0xFF for x in data["imagem"]))
    imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")

    return token_desafio, imagem_base64

token, imagem_base64 = load_captcha()
print("Token Desafio:", token)
print("Imagem em Base64:", imagem_base64)
image_data = base64.b64decode(imagem_base64)
image = Image.open(io.BytesIO(image_data))
image.save('output_image.png')


import requests

url = "https://cndt-certidao.tst.jus.br/inicio.faces"

payload='j_id_jsp_992698495_2=j_id_jsp_992698495_2&j_id_jsp_992698495_2%3Aj_id_jsp_992698495_3=Emitir%2BCertid%C3%A3o&javax.faces.ViewState={}'.format(viewstate.replace('/','%2F').replace('+','%2B').replace('=','%3D'))
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'JSESSIONID={}; 7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR;'.format(response.cookies.get_dict()['JSESSIONID'],response.cookies.get_dict()['7aa721eeaef392956e2c4add5997cdb0']),
  'Origin': 'https://cndt-certidao.tst.jus.br',
  'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces',
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
























import requests

url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

payload={}
headers = {
  'authority': 'pje1g.trf3.jus.br',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'cookie': 'MO=P; JSESSIONID2=dXmdUdwG2KvCAazmT5rBbcTVXYGPtfuDhJq0zsPz.svlpje21g14; PJECSID=ebcb5090ef97b5a6; PJESID=3f321c0ad7a8c69a; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQdxY2F9TCnbqJAQAA5Xr9wRQAiZFcJCu58wUsOY7ReD43kP6qypupn5+CEXH++dkvU5Y0icJFmZqNlzDeit2s4ecvl8HVsY3UCAYXPUcodVgtVb9aXmuJZjFjRAT14B/bcBMLLK1CCVmjUUv+MQ18IB9sSU/6Ie/DgGXF9ZBTUM2ulyn+3pqRdIZKG6i8LTArwuLlMEACeoOBODEQydP4c3v7LR1c06hlVnVCW+pdfSEsJxLo768Q/sDhVDFbpuGh/5IMneqWm69bf0qWw4i6UmnqXkwsm4+LwfkEXPh1r71UlcFUYs6MNoIASD8AtPX9rHYa7vEhqeKGAJY41mOauNLk8Ry7O7c16JLVOcnr9cU4deeeYSlPiRH1zZ1rIBczPPAU67ZbKR697V93TxKgEtpVA7Npc73aWOd0bOQxRtx36j0x8QSD/PN4kwLE33SSNVNGqlddZ4nhpOeoEGUJjEaGg4Y/nV36lM5LP0oQWoZSHlvmlaoo; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQdxY2FxfUnbqJAQAAIYAlwhTU3aN+AGsIlvdfcAvScDPViouEZK5h9AEH/i8cV6EMv9zBfcq87gvgyx3EnC3akg80tOlbqLPBre0/V54TSMdzEnWk/chsBCgQyAJWChpYKjoCdmzkIDtdbUxZESmGKIRk/rZsfRMRaiRevzzOjpKYsiyC4NABkwlluO2dzAx+ilE60nkiAcGANi0MeUf9bQG4aa1WMLPXvn+Eu0ruARPJUsUrsgzGiWtCco56iQ==~1; JSESSIONID=prLlPTNHhn9G58YR7SM7pH5QfDXu0uTWZCfqS_am.svlpje1g07; JSESSIONID2=pvb5rRh3E4OeB9tHnkrt19eGIQMzjxS_uxdnVDb3.svlpje21g14; MO=P; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQlNXaF06VnXGJAQAAr0Q9whTK3VOdyl6WFvCaH6H2yb2qfaaSNtXxtW8yz8c8nJcntTgPevs9whmwyFiLZBKcUSi179gePN9ec7ihSg3MMN8EwXTXJbJlcyZNQ8HoMNcuBFcM1NhHChAA4vOw+I/BuVXAmkZy/e9bYis6eLn674wAB+cHYROrt3zE40C3fmVBjvMybV8B4sWRtDYc0lp4iEQPlF7PUGZB1ADFUvbBcxtv4D6/taaTn+9N+V9XHUvt/Gk2T15GSlF1KUhNTLNTrIZA3BQ+7tZ8pQk9rl6/FbAdvg2ir55mvnLIs699PP72iGZ7ROh6QOjy6/lzjjpGc81IIuMCmI7e3ytmpdBN39N4TMSyofUECaF1BQGCgnOAdEsrtOmF4YhBTDFSTmvgLB1GB2HjOmysFr99vaG8KwtDeJOVQ9fhHzTbpcq2jPNp/zeWAaM2LWSFjh+7ojKw5VcAgTrpbrxL9FUGO3T2UPkFgqkhEeYtd/NPHzRseIAVm+IdIG8VeW/uU+kuaXHJUWxA21IaOc1VmnuZpnNr; bm_mi=37A7AD95AA469BB60F7E312E701246AB~YAAQTsQUAqQ3PG6JAQAAKD4AwhSxUihZJgtCjNQVNZTUB0SnVhHclJgZ8pqGgPYayy+C0uYDJTs6J/qb3uxEvFfEn10GxDK6KCZ8F2COtkTSPrf5CRethwXtDuSfGnDQaW04IvN47iWGxpLyyTMRIS8IFkLkfiQLg+nafdkKfss83NxR+lst3UePI0Ai1nXi0lTfiqpHNT8mQ8+NcMraztyoulQFzFWp0pJYaFFwwJI4ZCi05wWrv0i6ROqPW9HxS3aysYwj2S6QXseXZCq3fafSmSd7/oib+SkbcvTW+TS3nUKqk8XVL2IUjC7gJusdnAiNZF6AWKLt+21XNsMZSUp3AEjy1gpCdtFc7Ln0AA==~1; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQlNXaF0+VnXGJAQAAr0Q9whR5Vv+rqu/fsQWqUFF1TObYzfUbRUKJCTeQsNIZ05iguvOPc6c8SYWWGsILQCiL9cKhvWSZsAsSrmkoxWqMPr0FvxeicBTf5qJ7nv1M+2EzhEFZmrZNms/5q0oMTjmgevUMIBBQLkxdYWoSSD7IkjB+La+6oPMtgB4kY3YZL+Z7UiQ5ESy8QYi+6HXS8Jhhk9z8gGJtrYDT9nqzXiQFo+/yIdq2DreFY0kIg/+UpA==~1; PJECSID=29bfdcddb51f695c; PJESID=98bcb5ba410dd2c6',
  'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


import requests

url = "https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam"

payload = "AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso=&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id147%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id165%3AnomeAdv=&fPP%3Aj_id174%3AclasseProcessualProcessoHidden=&tipoMascaraDocumento=on&fPP%3AdpDec%3AdocumentoParte=000.000.000-00&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id209=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id4&fPP%3Aj_id215=fPP%3Aj_id215&AJAX%3AEVENTS_COUNT=1&"
headers = {
  'authority': 'pje1g.trf3.jus.br',
  'accept': '*/*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'MO=P; JSESSIONID2=dXmdUdwG2KvCAazmT5rBbcTVXYGPtfuDhJq0zsPz.svlpje21g14; PJECSID=ebcb5090ef97b5a6; PJESID=3f321c0ad7a8c69a; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQdxY2F9TCnbqJAQAA5Xr9wRQAiZFcJCu58wUsOY7ReD43kP6qypupn5+CEXH++dkvU5Y0icJFmZqNlzDeit2s4ecvl8HVsY3UCAYXPUcodVgtVb9aXmuJZjFjRAT14B/bcBMLLK1CCVmjUUv+MQ18IB9sSU/6Ie/DgGXF9ZBTUM2ulyn+3pqRdIZKG6i8LTArwuLlMEACeoOBODEQydP4c3v7LR1c06hlVnVCW+pdfSEsJxLo768Q/sDhVDFbpuGh/5IMneqWm69bf0qWw4i6UmnqXkwsm4+LwfkEXPh1r71UlcFUYs6MNoIASD8AtPX9rHYa7vEhqeKGAJY41mOauNLk8Ry7O7c16JLVOcnr9cU4deeeYSlPiRH1zZ1rIBczPPAU67ZbKR697V93TxKgEtpVA7Npc73aWOd0bOQxRtx36j0x8QSD/PN4kwLE33SSNVNGqlddZ4nhpOeoEGUJjEaGg4Y/nV36lM5LP0oQWoZSHlvmlaoo; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQdxY2F0DUnbqJAQAAw5ImwhSLHIffAZgL1S+IibQA9LvNnTurOJbKefwYEVGfs4P9DOP7RDoIOLMcBWtET/sjt9HGSQdRBatRzNUB4VRISVpBCmdmtSU+uReq7bbe/BIzqCWu6mYdK3AagbOHbEXZBf88wqNgcq6AxLxiPJj3+NgztDuj8t6732A+200NWuKFN3ywfIuLOXmehv6i0ET92mTiUi45acIinuayb0GZqbQSkL2YbkjQOLmHWdBdxg==~1; JSESSIONID=prLlPTNHhn9G58YR7SM7pH5QfDXu0uTWZCfqS_am.svlpje1g07; JSESSIONID2=pvb5rRh3E4OeB9tHnkrt19eGIQMzjxS_uxdnVDb3.svlpje21g14; MO=P; ak_bmsc=A742B514F1147C216E2B26A676D730C3~000000000000000000000000000000~YAAQlNXaF52VnXGJAQAACXU9whSeBK7Mz1T332abnrZc3GbUF5oJVpMu3hTH9vs+svTCDSOynG2AWRQ0LGSGBlGRYrjOxJG/4604VnGZmMc9RBq8SGm6RNtzNq2lnEvgnzH/7Y2gubC1ONyGeYqWfJ/HaAzuGHbOR8rZF2HuubNW/bi4uOO68VIOMJL4gSqNA+xx0AyRIouC9gYvImVdsxlbsOPHLRZ+AB1FgyreT49g06dPNyrz3PCBdXA0Ded2wPwDCnesadmhSD/1A5Ek9euzlYPnGx5wiKxMO9fnlFLZlc7elhHif1hFo0wQgk0bel4OVpuiqowIKbc1Djdzbl0cNoYD3FNEiVZNVjwkvagH9vso3APwW9DjJOB6+9LKpnpUsW61Q+2kYq0rAoD0RGiQFKPTN80oZm+fHKj0vDday7bZlFechnQbXLN0dIPyvs9UuscfFiWWvhN9CKSvGl1tG6Mss0qz/9/UpBmlQtkyORlIQ68OdElBvnL0D8G3r62o36P5xidPgeRkBAnQcr/vq9d15menAGjmjDFxVaft; bm_mi=37A7AD95AA469BB60F7E312E701246AB~YAAQTsQUAqQ3PG6JAQAAKD4AwhSxUihZJgtCjNQVNZTUB0SnVhHclJgZ8pqGgPYayy+C0uYDJTs6J/qb3uxEvFfEn10GxDK6KCZ8F2COtkTSPrf5CRethwXtDuSfGnDQaW04IvN47iWGxpLyyTMRIS8IFkLkfiQLg+nafdkKfss83NxR+lst3UePI0Ai1nXi0lTfiqpHNT8mQ8+NcMraztyoulQFzFWp0pJYaFFwwJI4ZCi05wWrv0i6ROqPW9HxS3aysYwj2S6QXseXZCq3fafSmSd7/oib+SkbcvTW+TS3nUKqk8XVL2IUjC7gJusdnAiNZF6AWKLt+21XNsMZSUp3AEjy1gpCdtFc7Ln0AA==~1; bm_sv=F64F409FD216FD31D0603E3EF8501DE9~YAAQlNXaF0+VnXGJAQAAr0Q9whR5Vv+rqu/fsQWqUFF1TObYzfUbRUKJCTeQsNIZ05iguvOPc6c8SYWWGsILQCiL9cKhvWSZsAsSrmkoxWqMPr0FvxeicBTf5qJ7nv1M+2EzhEFZmrZNms/5q0oMTjmgevUMIBBQLkxdYWoSSD7IkjB+La+6oPMtgB4kY3YZL+Z7UiQ5ESy8QYi+6HXS8Jhhk9z8gGJtrYDT9nqzXiQFo+/yIdq2DreFY0kIg/+UpA==~1; PJECSID=29bfdcddb51f695c; PJESID=98bcb5ba410dd2c6',
  'origin': 'https://pje1g.trf3.jus.br',
  'referer': 'https://pje1g.trf3.jus.br/pje/ConsultaPublica/listView.seam',
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


























resposta = ''

url = "https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf"

payload='emitirCrda=emitirCrda&emitirCrda%3AcrdaInputCnpjBase=&emitirCrda%3AcrdaInputCpf=403.154.468-54&g-recaptcha-response={}&emitirCrda%3Aj_id97=Emitir&javax.faces.ViewState=j_id1'.format(resposta)
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'JSESSIONID={};'.format(JSESSIONID),
  'Origin': 'https://www.dividaativa.pge.sp.gov.br',
  'Referer': 'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf?param=150304',
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

captcha = Solve_Captcha()
response = captcha.recaptcha('6Le9EjMUAAAAAPKi-JVCzXgY_ePjRV9FFVLmWKB_','https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf;jsessionid=72B376078823BBC593503156E614391E.395015-sc-03')

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
    print(response.text)
    sitekey = response.text.split('data-sitekey=')[1].split('\r')[0].replace('"','')
else:
    print(f"Erro {response.status_code} ao fazer a solicitação")

# Fechar a instância do cliente HTTP
client.close()

captcha = Solve_Captcha()
response = captcha.recaptcha(sitekey,'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario')

url = "https://www2.ssp.sp.gov.br/aacweb/emitir-atestado.action"
'''payload = {
    "nome": "ALINE EMILY TIOMI LENSARINI TOMIMURA",
    "numero": "54918611",
    "digito": "6",
    "txtDIAE": "11",
    "txtMESE": "10",
    "txtANOE": "2019",
    "sexo": "F",
    "txtDIA": "24",
    "txtMES": "04",
    "txtANO": "1994",
    "nomePai": "CARLOS TOMOYASHU TOMIMURA",
    "nomeMae": "ROSA MARIA LENSARINI TOMIMURA",
    "g-recaptcha-response": response,  # Adicione o valor correto aqui
    "pesquisa": "Pesquisar"
}'''
payload = {
    "nome": "WESLEY SILVA CABRAL DE OLIVEIRA",
    "numero": "48788239",
    "digito": "8",
    "txtDIAE": "26",
    "txtMESE": "03",
    "txtANOE": "2003",
    "sexo": "M",
    "txtDIA": "14",
    "txtMES": "11",
    "txtANO": "1992",
    "nomePai": "ANTONIO CABRAL DE OLIVEIRA",
    "nomeMae": "JULIENE MARIA DA SILVA",
    "g-recaptcha-response": response,  # Adicione o valor correto aqui
    "pesquisa": "Pesquisar"
}
#payload='nome=WESLEY%20SILVA%20CABRAL%20DE%20OLIVEIRA&numero=48788239&digito=8&txtDIAE=26&txtMESE=03&txtANOE=2003&sexo=M&txtDIA=14&txtMES=11&txtANO=1992&nomePai=ANTONIO%20CABRAL%20DE%20OLIVEIRA&nomeMae=JULIENE%20MARIA%20DA%20SILVA&g-recaptcha-response={}&pesquisa=Pesquisar'.format(response)
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

if response.headers.get("content-type") == "application/pdf":
    with open("arquivo.pdf", "wb") as pdf_file:
        pdf_file.write(response.content)
    print("Arquivo PDF salvo com sucesso.")
else:
    pdf_file_path = os.path.join('/opt/projetos/original/certidoes','antecedentes.pdf')
    pdfkit.from_string(response.text.replace('/AACWEBSTATIC/img/imp_cab.gif','https://www2.ssp.sp.gov.br/AACWEBSTATIC/img/imp_cab.gif'), pdf_file_path, options={'encoding': 'utf-8'})
    print("Arquivo PDF salvo com sucesso.")
