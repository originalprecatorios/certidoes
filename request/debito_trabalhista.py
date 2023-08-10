import requests
import os
import base64
from PIL import Image
import io

class Debito_trabalhista():
    def __init__(self,pData,pCaptcha):
        print('Debito Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        if os.path.isdir('{}'.format(self._data['path'])):
            print("O diretório existe!")
        else:
            os.makedirs('{}'.format(self._data['path']))
    
    def get_cookies(self):
        response = requests.get('https://cndt-certidao.tst.jus.br/inicio.faces')
        self._jsessionid = response.cookies.get('JSESSIONID')
        self._id = response.cookies.get_dict()['7aa721eeaef392956e2c4add5997cdb0']
        self._viewstate = response.text.split('javax.faces.ViewState:0" value="')[1].split('"')[0].replace('/','%2F').replace('+','%2B').replace('=','%3D')
        self._jd_id = 'j_id_jsp_'+response.text.split('name="j_id_jsp_')[1].split('"')[0]
        
    def image_captcha(self):
        url = "https://cndt-certidao.tst.jus.br/api"

        payload={}
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID={}; 7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR;'.format(self._jsessionid,self._id),
        'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces;jsessionid={}'.format(self._jsessionid),
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

        self._token_desafio = data["tokenDesafio"]

        imagem_bytes = bytes((x & 0xFF for x in data["imagem"]))
        imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")

        image_data = base64.b64decode(imagem_base64)
        image = Image.open(io.BytesIO(image_data))
        image.save(os.path.join(self._data['path'],'captcha.png'))

    def get_download(self):
        self.get_cookies()

        url = "https://cndt-certidao.tst.jus.br/inicio.faces"

        payload='j_id_jsp_992698495_2=j_id_jsp_992698495_2&j_id_jsp_992698495_2%3Aj_id_jsp_992698495_3=Emitir%2BCertid%C3%A3o&javax.faces.ViewState={}'.format(self._viewstate)
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.409603520.1691609614; _gid=GA1.3.62502923.1691609614; _ga_XKVCLCWXBN=GS1.3.1691609614.1.1.1691609616.0.0.0; JSESSIONID={};'.format(self._id,self._jsessionid),
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
        self._viewstate = response.text.split('javax.faces.ViewState:0" value="')[1].split('"')[0].replace('/','%2F').replace('+','%2B').replace('=','%3D')

        self.image_captcha()
        captcha_response = self._captcha.resolve_normal(os.path.join(self._data['path'],'captcha.png'))
        #captcha_response = ''
        os.system('rm {}'.format(os.path.join(self._data['path'],'captcha.png')))

        

        url = "https://cndt-certidao.tst.jus.br/gerarCertidao.faces"

        payload = "AJAXREQUEST=j_id_jsp_216541370_0&gerarCertidaoForm=gerarCertidaoForm&gerarCertidaoForm%3ApodeFazerDownload=false&gerarCertidaoForm%3AcpfCnpj=235.129.258-80&resposta={}&tokenDesafio={}&emailUsuario=&javax.faces.ViewState={}&gerarCertidaoForm%3AbtnEmitirCertidao=gerarCertidaoForm%3AbtnEmitirCertidao&".format(captcha_response,self._token_desafio,self._viewstate)
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.409603520.1691609614; _gid=GA1.3.62502923.1691609614; _ga_XKVCLCWXBN=GS1.3.1691609614.1.1.1691609616.0.0.0; JSESSIONID={};'.format(self._id,self._jsessionid),
        'Origin': 'https://cndt-certidao.tst.jus.br',
        'Referer': 'https://cndt-certidao.tst.jus.br/inicio.faces',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.text.find('Aguarde') >=0:

            url = "https://cndt-certidao.tst.jus.br/emissaoCertidao?pfnc=5897495482149488"

            payload={}
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': '7aa721eeaef392956e2c4add5997cdb0={}; INSTANCIA=cndt-certidao; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.409603520.1691609614; _gid=GA1.3.62502923.1691609614; _ga_XKVCLCWXBN=GS1.3.1691609614.1.1.1691609616.0.0.0; JSESSIONID={}'.format(self._id,self._jsessionid),
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

            response = requests.request("GET", url, headers=headers, data=payload)
            if response.headers.get("content-type") == "application/pdf":

                with open(os.path.join(self._data['path'],'12- CERTIDÃO DE DÉBITOS TRABALHISTAS.pdf'), 'wb') as f:
                    f.write(response.content)
                
                for arquivo in os.listdir(self._data['path']):
                    if arquivo.find('12- CERTIDÃO DE DÉBITOS TRABALHISTAS.pdf') > -1:
                        print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                        return
                    print('Download concluido')
            
            raise ValueError
        
        raise ValueError
        
        