import requests
import os
import pdfkit
from bs4 import BeautifulSoup
from weasyprint import HTML

class Ipva_estadual:
    def __init__(self,pData,pCaptcha):
        self._data = pData
        self._captcha = pCaptcha
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
    
    def get_cookies(self):
        x = requests.request("GET", 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx')
        cookie = x.cookies.get_dict()
        self._cookies = '_ga_7RC6MLS8YN=GS1.1.1683597623.5.0.1683597631.0.0.0; _ga=GA1.1.825311961.1661543027; ASP.NET_SessionId={}; TS01308bf5={}; ai_user=7esZ8|2023-07-17T23:00:26.023Z; ai_session=WTFaP|1689685165042|1689685173137'.format(cookie['ASP.NET_SessionId'],cookie['TS01308bf5'])
        soup = BeautifulSoup(x.text, "html.parser")
        self._viewstate_generator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"].replace('/','%2F').replace('+','%2B').replace('=','%3D')
        self._event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"].replace('/','%2F').replace('+','%2B').replace('=','%3D')
        self._viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"].replace('/','%2F').replace('+','%2B').replace('=','%3D')
        self._sitekey = x.text.split('data-sitekey=')[1].split('>')[0].replace('"','')
        self._response = self._captcha.recaptcha(self._sitekey,'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/consulta.aspx')

    def send_data(self):
        url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Consulta.aspx"
        payload='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&__EVENTVALIDATION={}&ctl00%24conteudoPaginaPlaceHolder%24txtRenavam={}&ctl00%24conteudoPaginaPlaceHolder%24txtPlaca={}&g-recaptcha-response={}&ctl00%24conteudoPaginaPlaceHolder%24btn_Consultar=Consultar'.format(self._viewstate,self._viewstate_generator,self._event_validation,self._data['renavan'],self._data['placa'].replace('-',''),self._response)       
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.ipva.fazenda.sp.gov.br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
        'Cookie': self._cookies,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    
    def creat_pdf(self):
        url = "https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/Pages/Aviso.aspx"

        payload={}
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.ipva.fazenda.sp.gov.br/ipvanet_consulta/EncerrarSessao.aspx',
        'Connection': 'keep-alive',
        'Cookie': self._cookies,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        pdf_file_path = os.path.join(self._data['path'],'ESTADUAL IPVA.pdf')
        try:
            HTML(string=response.text).write_pdf(pdf_file_path)
            #pdfkit.from_string(response.text, pdf_file_path, options={'encoding': 'utf-8'})
        except:
            pass
        print(f"Arquivo PDF salvo em: {pdf_file_path}")

        for arquivo in os.listdir(self._data['path']):
            if arquivo.find('ESTADUAL IPVA.pdf') > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return
        
        raise ValueError("Nenhum documento encontrado")