import requests
import os, time
from selenium.webdriver.common.by import By
from utils.selenium_classes import Selenium_classes

class Trabalhista:
    def __init__(self,pData,pCaptcha,pLink):
        print('Robo Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        self._cont = 0
        self._link = pLink
        self.navegation = Selenium_classes(self._data['path'])
        self.navegation.firefox(self._link,None)
        
        
    def login(self):
        self._capt = '/tmp/captcha/'
        if os.path.isdir(f'{self._capt}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._capt}')
        
        cookie = self.navegation.cookies()
        co = "PHPSESSID={}; _ga={}; _gid={}; ww2.trtsp.jus.br={}; contraste={}; fontes={}; escalabilidade={}".format(cookie[0]['value'],cookie[1]['value'],cookie[2]['value'],cookie[4]['value'],cookie[5]['value'],cookie[6]['value'],cookie[7]['value'])
        response = self.solve_cap()
        id_captcha  = self.navegation.wait_element('NAME','captcha[id]').get_attribute('value')
        self.navegation.close_driver()

        try:
            url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao"

            payload='tipoDocumentoPesquisado=1&numeroDocumentoPesquisado={}&nomePesquisado={}&jurisdicao=0&periodo=1&data_inicial=&data_final=&captcha%5Bid%5D={}&captcha%5Binput%5D={}&submit=&submit='.format(self._data['cpf'],self._data['nome'],id_captcha,response)
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://aplicacoes10.trt2.jus.br',
            'Connection': 'keep-alive',
            'Cookie': co,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/recuperarcertidao"

            payload={}
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/imprimecertidao',
            'Connection': 'keep-alive',
            'Cookie': co,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            if response.headers.get("content-type") == "application/pdf":
                with open(os.path.join(self._data['path'],'11- TRT2ª.pdf'), "wb") as pdf_file:
                    pdf_file.write(response.content)
                print("Arquivo PDF salvo com sucesso.")
            else:
                self.navegation.close_driver()
                raise ValueError

            
            for arquivo in os.listdir(self._data['path']):
                if arquivo.find('11- TRT2ª.pdf') > -1:
                    print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                    return
            
            self.navegation.close_driver()
            raise ValueError
            
        except:
            self.navegation.close_driver()
            return

    def solve_cap(self):
        self.navegation.wait_element('CLASS_NAME','tcaptcha')
        with open(f'{self._capt}captcha.png', 'wb') as file:
            l = self.navegation.element('CLASS_NAME','tcaptcha').find_element(By.TAG_NAME,'img')
            file.write(l.screenshot_as_png)
        time.sleep(1)
        response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
        if response is None:
            response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
        #response = ''
        os.system('rm {}'.format(os.path.join(self._capt,'captcha.png')))
        return response
        
