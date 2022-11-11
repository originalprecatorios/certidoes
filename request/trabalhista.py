from bs4 import BeautifulSoup
import requests
import shutil,os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class Trabalhista:
    def __init__(self,pData,pCaptcha,pLink):
        print('Robo Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        self._cont = 0
        self._link = pLink

        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        cooki = self._driver.get_cookies()
        self._cookies = {
            'Cookie': "PHPSESSID={}; _ga={}; _gid={}; ww2.trtsp.jus.br={}; contraste={}; fontes={}; escalabilidade={}; _gat=1".format(cooki[0]['value'],cooki[1]['value'],cooki[2]['value'],cooki[4]['value'],cooki[5]['value'],cooki[6]['value'],cooki[7]['value'])
        }
        
    def login(self):
        self._capt = '/tmp/captcha/'
        if os.path.isdir(f'{self._capt}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._capt}')

        self._pasta = self._data['path']
        #self._pasta = '/opt/certidao/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')

        try:
            url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao"

            payload={}
            headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/imprimecertidao',
            'Connection': 'keep-alive',
            'Cookie': '{}'.format(self._cookies['Cookie']),
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            

            soup = BeautifulSoup(response.text, 'html.parser')
            captcha_id = soup.find(id="captcha-id").get('value')
            url = 'https://aplicacoes10.trt2.jus.br' + soup.find("table", {"class": "tcaptcha"}).find_all("img")[0].get('src')
            response = requests.get(url, stream=True)
            with open(self._capt+'captcha.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            solve_captcha = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            os.system('rm {}'.format(os.path.join(self._capt,'captcha.png')))

            url = "https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao"

            payload='tipoDocumentoPesquisado=1&numeroDocumentoPesquisado={}&nomePesquisado={}&jurisdicao=0&periodo=1&data_inicial=&data_final=&captcha%5Bid%5D={}&captcha%5Binput%5D={}&submit=&submit='.format(self._data['cpf'],self._data['nome'].strip(),captcha_id,solve_captcha)
            headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://aplicacoes10.trt2.jus.br',
            'Connection': 'keep-alive',
            'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao',
            'Cookie': '{}'.format(self._cookies['Cookie']),
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
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/imprimecertidao',
            'Cookie': '{}'.format(self._cookies['Cookie']),
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            

            with open(self._pasta+'11- TRT2ª.pdf', 'wb') as f:
                f.write(response.content)
            self._driver.close()
        except:
            self._cont += 1
            if self._cont <= 3:
                self.login()
            else:
                return

        
