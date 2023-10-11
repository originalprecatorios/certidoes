import requests
import os, time
from selenium.webdriver.common.by import By
from utils.selenium_classes import Selenium_classes

class Trt15:
    def __init__(self,pData,pCaptcha,pLink):
        print('Robo Trabalhista')
        self._data = pData
        self._captcha = pCaptcha
        self._cont = 0
        self._link = pLink
        self.create_folder(self._data['path'])
        #self.navegation = Selenium_classes(self._data['path'])
        #try:
        #    self.navegation.firefox('https://ceat.trt15.jus.br/ceat/seam/resource/captcha?f=1690828042005',None)
        #except:
        #    self.navegation.close_driver()
        #    raise ValueError
        #self.navegation.accept_cookie()
    
    # Cria uma pasta conforme passado no parametro
    def create_folder(self,pPath):
        self.print_colored("Criando pasta", "blue")
        if os.path.isdir(f'{pPath}'):
            self.print_colored("O diretório existe!", "red")
        else:
            os.makedirs(f'{pPath}')
            self.print_colored("Diretório Criado!", "green")
        
    def login(self):
        try:
            print('login')
            time.sleep(2)
            url = "https://ceat.trt15.jus.br/ceat/seam/resource/captcha?f=1690828042005"

            payload={}
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            cookie = response.cookies.get_dict()['JSESSIONID']
            #cookie = self.navegation.cookies()

            url = "https://ceat.trt15.jus.br/ceat/certidaoAction.seam"

            payload={}
            #headers = {
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            #'Cookie': 'JSESSIONID={}'.format(cookie[0]['value'])
            #}

            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Cookie': 'JSESSIONID={}'.format(cookie)
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            # URL para obter a imagem do captcha
            url_captcha = "https://ceat.trt15.jus.br/ceat/seam/resource/captcha?f=1690828042005"

            # Headers necessários para a solicitação
            headers = {
                'authority': 'ceat.trt15.jus.br',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'cookie': 'JSESSIONID={}; _ga=GA1.1.2084834512.1690570491; _ga_HMMN3T1GVL=GS1.1.1690573933.2.1.1690575809.0.0.0'.format(cookie),
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

            '''headers = {
                'authority': 'ceat.trt15.jus.br',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'max-age=0',
                'cookie': 'JSESSIONID={}; _ga=GA1.1.2084834512.1690570491; _ga_HMMN3T1GVL=GS1.1.1690573933.2.1.1690575809.0.0.0'.format(cookie[0]['value']),
                'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            }'''

            # Fazer a solicitação para obter a imagem do captcha
            response_captcha = requests.get(url_captcha, headers=headers)

            # Salvar a imagem em um arquivo local
            with open(os.path.join(self._data['path'],'captcha.jpg'), 'wb') as f:
                f.write(response_captcha.content)

            print("Imagem do captcha salva com sucesso!")
            response = self._captcha.resolve_normal(os.path.join(self._data['path'],'captcha.jpg'))
            time.sleep(1)
            print('passo pelo captcha')
            if response is None:
                response = self._captcha.resolve_normal(os.path.join(self._data['path'],'captcha.jpg'))
            #response = ''
            response = response.replace('=','')
            if '+' in response:
                soma = int(response.split('+')[0]) + int(response.split('+')[1])
            elif 'x' in response:
                soma = int(response.split('x')[0]) + int(response.split('x')[1])
            else:
                soma = int(response)
            soma = str(soma)
            os.system('rm {}'.format(os.path.join(self._data['path'],'captcha.jpg')))
            # URL para gerar a certidão
            url_certidao = "https://ceat.trt15.jus.br/ceat/certidaoAction.seam"

            # Dados do formulário para gerar a certidão (incluindo a resposta do captcha)
            payload_certidao = {
                'certidaoActionForm': 'certidaoActionForm',
                'certidaoActionForm:decTipoPesquisa:radiotipopesquisa': 'D',
                'certidaoActionForm:j_id23:doctoPesquisa': '{}'.format(self._data['cpf']),
                'certidaoActionForm:j_id33:nomePesquisa': '',
                'certidaoActionForm:j_id51:verifyCaptcha': soma,
                'certidaoActionForm:certidaoActionEmitir': 'Emitir Certidão',
                'javax.faces.ViewState': 'j_id1'
            }

            # Fazer a solicitação para gerar a certidão
            response_certidao = requests.post(url_certidao, headers=headers, data=payload_certidao)

            

            url_pdf = "https://ceat.trt15.jus.br/ceat/certidaoAction.seam"

            # Dados do formulário para baixar o arquivo em PDF
            payload_pdf = {
                'certidaoActionForm': 'certidaoActionForm',
                'certidaoActionForm:certidaoActionImprimir': 'Imprimir Certidão',
                'javax.faces.ViewState': 'j_id2'
            }

            # Fazer a solicitação para baixar o arquivo em PDF
            response_pdf = requests.post(url_pdf, headers=headers, data=payload_pdf)

            if response_pdf.headers.get("content-type") == "application/pdf":
                # Salvar o conteúdo do PDF em um arquivo local
                with open(os.path.join(self._data['path'],'14- TRT15ª.pdf'), 'wb') as f:
                    f.write(response_pdf.content)
                print("Certidão gerada com sucesso!")
                #self.navegation.close_driver()
            
            for arquivo in os.listdir(self._data['path']):
                if arquivo.find('14- TRT15ª.pdf') > -1:
                    print('Download concluido para o cpf {}'.format(self._data['cpf']))
                    return
            #self.navegation.close_driver()
            raise ValueError
        except:
            #self.navegation.close_driver()
            raise ValueError
    
    

        


































        cookie = self.navegation.cookies()
        self.navegation.navegation('https://ceat.trt15.jus.br/ceat/seam/resource/captcha?f=1690824314457')
        cookie = self.navegation.cookies()

        self.navegation.download_img(self._data['path'])
        
        #response = self._captcha.resolve_normal(os.path.join(self._data['path'],'captcha.png'))
        #response = ''
        time.sleep(1)
        response = response.replace('=','')
        if '+' in response:
            soma = int(response.split('+')[0]) + int(response.split('+')[1])
        elif 'x' in response:
            soma = int(response.split('x')[0]) + int(response.split('x')[1])
        else:
            soma = response

        soma = str(soma)    
        os.system('rm {}'.format(os.path.join(self._data['path'],'captcha.jpg')))

        

        url = "https://ceat.trt15.jus.br/ceat/certidaoAction.seam"

        payload='certidaoActionForm=certidaoActionForm&certidaoActionForm%3AdecTipoPesquisa%3Aradiotipopesquisa=D&certidaoActionForm%3Aj_id23%3AdoctoPesquisa=403.154.468-54&certidaoActionForm%3Aj_id33%3AnomePesquisa=&certidaoActionForm%3Aj_id51%3AverifyCaptcha={}&certidaoActionForm%3AcertidaoActionEmitir=Emitir%2BCertid%C3%A3o&javax.faces.ViewState=j_id2'.format(response)

        headers = {
        'authority': 'ceat.trt15.jus.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'JSESSIONID={}; _ga={}; _ga_HMMN3T1GVL={}'.format(cookie[0]['value'],cookie[3]['value'],cookie[5]['value']),
        'origin': 'https://ceat.trt15.jus.br',
        'referer': 'https://ceat.trt15.jus.br/ceat/certidaoAction.seam',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        url = "https://ceat.trt15.jus.br/ceat/certidaoAction.seam"

        payload='certidaoActionForm=certidaoActionForm&certidaoActionForm%3AcertidaoActionImprimir=Imprimir%2BCertid%C3%A3o&javax.faces.ViewState=j_id3'
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://ceat.trt15.jus.br/ceat/certidaoAction.seam',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://ceat.trt15.jus.br',
                'Connection': 'keep-alive',
                'Cookie': 'JSESSIONID={}; _ga={}; _ga_HMMN3T1GVL={}'.format(cookie[0]['value'],cookie[3]['value'],cookie[5]['value']),
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'iframe',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'TE': 'trailers'
                }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.headers.get("content-type") == "application/pdf":
                with open(os.path.join(self._data['path'],'14- TRT15ª.pdf'), "wb") as pdf_file:
                    pdf_file.write(response.content)
                print("Arquivo PDF salvo com sucesso.")
        else:
            self.navegation.close_driver()
            raise ValueError

        
        for arquivo in os.listdir(self._data['path']):
            if arquivo.find('14- TRT15ª.pdf') > -1:
                print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                return

























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
    
    # Cria um print com cor
    def print_colored(self, text, color):
        colors = {
            'blue': '\033[94m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'green': '\033[92m'
        }

        end_color = '\033[0m'

        if color.lower() in colors:
            colored_text = colors[color.lower()] + text + end_color
            print(colored_text)
        else:
            print("A cor selecionada não existe")
