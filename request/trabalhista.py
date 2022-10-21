from bs4 import BeautifulSoup
import requests
import shutil,os


class Trabalhista:
    def __init__(self,pData,pCaptcha):
        print('Robo Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        self._cont = 0
        
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
            'Cookie': 'PHPSESSID=kqd6a0n4n43ve8u1m8anu0u5k6; _ga=GA1.3.971099137.1658337294; _gid=GA1.3.1289141189.1658337294; ww2.trtsp.jus.br={%22contraste%22:0%2C%22fontes%22:1%2C%22escalabilidade%22:0}; contraste=0; fontes=1; escalabilidade=0; _gat=1',
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
            'Cookie': 'PHPSESSID=kqd6a0n4n43ve8u1m8anu0u5k6; _ga=GA1.3.971099137.1658337294; _gid=GA1.3.1289141189.1658337294; ww2.trtsp.jus.br={%22contraste%22:0%2C%22fontes%22:1%2C%22escalabilidade%22:0}; contraste=0; fontes=1; escalabilidade=0; _gat=1',
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
            'Cookie': 'PHPSESSID=kqd6a0n4n43ve8u1m8anu0u5k6; _ga=GA1.3.971099137.1658337294; _gid=GA1.3.1289141189.1658337294; ww2.trtsp.jus.br={%22contraste%22:0%2C%22fontes%22:1%2C%22escalabilidade%22:0}; contraste=0; fontes=1; escalabilidade=0; _gat=1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            

            with open(self._pasta+'_TRTSP.pdf', 'wb') as f:
                f.write(response.content)

        except:
            self._cont += 1
            if self._cont <= 3:
                self.login()
            else:
                return

        
