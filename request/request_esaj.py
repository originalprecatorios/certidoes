from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from decouple import config
import time, os, shutil
import requests
import magic
import io

class Request_esaj:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Robo Esaj')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')
        self._pasta = self._data['path']
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
    
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        
        
    def login(self):
        try:    
            self._driver.get(config('ESAJ_PAGE_LOGIN')) 
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "usernameForm")))
            self._driver.find_element(By.ID,"usernameForm").send_keys(f"{config('ESAJ_USER')}")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "passwordForm")))
            self._driver.find_element(By.ID,"passwordForm").send_keys(f"{config('ESAJ_PASS')}")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "pbEntrar")))
            self._driver.find_element(By.ID,"pbEntrar").click()
            time.sleep(5)
            self._driver.get(config('PAGE_URL_CRIMINAL_1'))
            time.sleep(2)
            self._cookies = 'JSESSIONID={}; K-JSESSIONID-bocbpjmm={}; __utma={}; __utmc={}; __utmz={}; __utmt={};__utmb={}'.format(self._driver.get_cookies()[0]['value'],self._driver.get_cookies()[1]['value'],self._driver.get_cookies()[4]['value'],self._driver.get_cookies()[2]['value'],self._driver.get_cookies()[5]['value'],self._driver.get_cookies()[3]['value'],self._driver.get_cookies()[6]['value'])
        
        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            
            return
    
    
    def solicita_arquivo(self,pSelect):
        url = "https://esaj.tjsp.jus.br/sco/salvarCadastro.do"
        
        if pSelect == '6':
            data_formatada = self._data['nascimento'][8:]+'%2F'+self._data['nascimento'][5:7]+'%2F'+self._data['nascimento'][:4]
            payload='pedidoIntranet=false&entity.cdModelo={}&entity.tpPessoa=F&entity.tpPessoa=F&entity.nmPesquisa={}&entity.nuCpfFormatado={}&entity.nuRgFormatado={}&entity.nuRgDig=&entity.flGenero={}&entity.nmMae={}&entity.nmPai=&entity.dtNascimento={}&entity.naturalidade.cdMunicipio=&entity.naturalidade.nmMunicipio=&entity.naturalidade.cdUf=&entity.solicitante.deEmail={}&confirmacaoInformacoes=true'.format(pSelect,self._data['nome'],self._data['cpf'],self._data['rg'],self._data['sexo'], self._data['mae'],data_formatada,self._data['email'].replace('@','%40'))
        else: 
            
            payload='pedidoIntranet=false&entity.cdModelo={}&entity.tpPessoa=F&entity.tpPessoa=F&entity.nmPesquisa={}&entity.nuCpfFormatado={}&entity.nuRgFormatado={}&entity.nuRgDig=&entity.flGenero={}&entity.solicitante.deEmail={}&confirmacaoInformacoes=true'.format(pSelect,self._data['nome'],self._data['cpf'],self._data['rg'],self._data['sexo'],self._data['email'].replace('@','%40'))
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': self._cookies,
        'Origin': 'https://esaj.tjsp.jus.br',
        'Referer': 'https://esaj.tjsp.jus.br/sco/abrirCadastro.do?gateway=true',
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
    
    def verifica_pedido(self):
        url = "https://esaj.tjsp.jus.br/sco/abrirResultadoCadastro.do"

        payload={}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': self._cookies,
        'Referer': 'https://esaj.tjsp.jus.br/sco/abrirCadastro.do?gateway=true',
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
        self._arr = {'numero_pedido' : response.text.replace('\n','').replace('\t','').split('class=""')[4].split('>')[1][:8],'data_pedido' : response.text.replace('\n','').replace('\t','').split('class=""')[7].split('>')[1][:10]}

        print(self._arr)
    
    def download_arquivo(self,pSelect):
        url = "https://esaj.tjsp.jus.br/sco/realizarDownload.do"

        payload='conversationId=&flSegundaVia=N&entity.nuPedido={}&entity.dtPedido={}&entity.tpPessoa=F&entity.nuCpfFormatado={}&entity.nuRgFormatado={}&entity.nuCnpjFormatado=&entity.nmPesquisa={}&pbConsultar=Consultar'.format(self._arr['numero_pedido'],self._arr['data_pedido'].replace('/','%2F'),self._data['cpf'],self._data['rg'],self._data['nome'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://esaj.tjsp.jus.br/sco/realizarDownload.do',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://esaj.tjsp.jus.br',
            'Connection': 'keep-alive',
            'Cookie': self._cookies,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
            }

        response = requests.request("POST", url, headers=headers, data=payload)


        file = io.BytesIO(response.content)

        # Usa a biblioteca magic para verificar o tipo de arquivo
        file_type = magic.from_buffer(file.read(2048), mime=True)

        # Verifica se o tipo de arquivo é um PDF
        if file_type == 'application/pdf':
            
            with open(f"{self._pasta}{pSelect}- ESAJ.pdf", 'wb') as f:
                f.write(response.content)
            
            for arquivo in os.listdir(self._pasta):
                if arquivo.find(f'{pSelect}- ESAJ.pdf') > -1:
                    print('Download concluido')        
                    self._driver.close()
                    return self._arr,True
            self._driver.close()
            self._driver.close()
        else:
            if len(self._arr['numero_pedido']) == 8:
                return self._arr,False
            else:
                self._driver.close()
                self._driver.close()
    
    def close_all(self):
        time.sleep(2)
        janelas = self._driver.window_handles

        # feche cada aba aberta
        for janela in janelas:
                self._driver.switch_to.window(janela)
                self._driver.close()
                time.sleep(2)