import httpx
import os
import pdfkit
import time

class Antecedentes_criminais:
    def __init__(self,pData,pCaptcha):
        self._data = pData
        self._captcha = pCaptcha
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
    
    def get_cookies(self):
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
            
            self._sitekey = response.text.split('data-sitekey=')[1].split('\r')[0].replace('"','')
        else:
            print(f"Erro {response.status_code} ao fazer a solicitação")

        # Fechar a instância do cliente HTTP
        client.close()
        self._response = self._captcha.recaptcha(self._sitekey,'https://www2.ssp.sp.gov.br/aacweb/carrega-formulario')
    
    def creat_pdf(self):
        url = "https://www2.ssp.sp.gov.br/aacweb/emitir-atestado.action"
        payload = {
            "nome": self._data['nome'],
            "numero": self._data['rg'][:-1],
            "digito": self._data['rg'][-1:],
            "txtDIAE": self._data['data_expedicao'].split('-')[2],
            "txtMESE": self._data['data_expedicao'].split('-')[1],
            "txtANOE": self._data['data_expedicao'].split('-')[0],
            "sexo": self._data['sexo'],
            "txtDIA": self._data['nascimento'].split('-')[2],
            "txtMES": self._data['nascimento'].split('-')[1],
            "txtANO": self._data['nascimento'].split('-')[0],
            "nomePai": self._data['pai'] if 'pai' in self._data else "",
            "nomeMae": self._data['mae'],
            "g-recaptcha-response": self._response,
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

        pdf_file_path = os.path.join(self._data['path'],'ANTECEDENTES CRIMINAIS.pdf')
        if response.headers.get("content-type") == "application/pdf":
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(response.content)
            print("Arquivo PDF salvo com sucesso.")
        else:
            try:
                pdfkit.from_string(response.text.replace('/AACWEBSTATIC/img/imp_cab.gif','https://www2.ssp.sp.gov.br/AACWEBSTATIC/img/imp_cab.gif'), pdf_file_path, options={'encoding': 'utf-8'})
            except:
                pass
            print("Arquivo PDF salvo com sucesso.")
        
        for arquivo in os.listdir(self._data['path']):
            if arquivo.find('ANTECEDENTES CRIMINAIS.pdf') > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return
        
        raise ValueError("Nenhum documento encontrado")