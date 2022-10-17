from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import time, os, shutil
from recaptcha.captcha import Solve_Captcha
import undetected_chromedriver as uc

class Federal:

    def __init__(self,pData,pLink,pMongo, pError,pCnpj):
        print('Federal')
        self._data = pData
        self._link = pLink
        self._cnpj = pCnpj
        self._bdMongo = pMongo
        self._error = pError
        self._error._getcoll('error')
        self._save = '/opt/certidao/download/'
        self._pasta = '/opt/certidao/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
            os.makedirs(f'{self._save}')

        '''
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self._pasta)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        fp.set_preference("pdfjs.disabled", True)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        self._driver.delete_all_cookies()
        set_cookie = str(self._request.headers).split('Set-Cookie')[1].split(';')[0].replace(':','').replace("'",'').strip()
        expiret = str(self._request.headers).split('expires')[1].split(';')[0].replace(':','').replace("'",'').replace('=','').strip()
        self._driver.add_cookie({'name': 'ASP.NET_SessionId', 'value': 'faozoqgfai2fsoi1hgxkral1', 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'Lax'})
        self._driver.add_cookie({'name': 'BIGipServerPOOL_SERVICO_RECEITA', 'value': '1541903521.47873.0000', 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': True, 'httpOnly': True, 'sameSite': 'None'})
        self._driver.add_cookie({'name': 'fileDownload', 'value': 'true', 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'})
        self._driver.add_cookie({'name': 'Set-Cookie', 'value': '{}'.format(set_cookie), 'expires':'{}'.format(expiret), 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'})
        link = 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni={}'.format(self._cnpj.replace('.','').replace('-',''))
        time.sleep(1)
        self._driver.get(link)
        time.sleep(5)
        '''
        
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        #self._driver = uc.Chrome(options=options,version_main=105)
        self._driver = uc.Chrome(options=options,version_main=89)
        #MUDAR A PARSTA DE DOWNLOAD
        params = {
            "behavior": "allow",
            "downloadPath": self._save
        }

        self._driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
        self._driver.get(self._link)
        self._driver.execute_script("window.stop();")
        
    
    def login(self):
        
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(self._cnpj)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "validar"))).click()
            time.sleep(2)
            #self._driver.execute_script("window.stop();")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "FrmSelecao")))
            self._driver.find_element(By.ID,"FrmSelecao").find_elements(By.TAG_NAME,"a")[1].click()
            time.sleep(10)
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
            if self._driver.find_element(By.ID,'main').text.find('A certidão foi emitida com sucesso') >= 0:
                self._download()
                archive_name = os.listdir(self._save)[0]
                shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}_CND_FEDERAL.pdf")
                print('Download concluido para o cpf {}'.format(self._cnpj))
            else:
                WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "rfb-main-container")))
                self._driver.find_element(By.ID,"rfb-main-container").find_element(By.TAG_NAME,"a").click()
                time.sleep(2)
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(self._cnpj)
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "validar"))).click()
                time.sleep(2)
                self._download()
                archive_name = os.listdir(self._save)[0]
                shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}_CND_FEDERAL.pdf")
                print('Download concluido para o cpf {}'.format(self._cnpj))
                    
            
            self._driver.close()
            
        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            return
    
    def solve_cap(self):
        try:
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
            with open(f'{self._capt}captcha.png', 'wb') as file:
                l = self._driver.find_element(By.TAG_NAME,'img')
                file.write(l.screenshot_as_png)

            response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            if response is None:
                response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            #response = ''
            os.system('rm {}'.format(os.path.join(self._capt,'captcha.png')))
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "ans")))
            self._driver.find_element(By.ID, 'ans').send_keys(response)
            time.sleep(2)
            
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "jar")))
            self._driver.find_element(By.ID, 'jar').click()
     
            time.sleep(3)
        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função solve_cap',
            }
            self._error.addData(err)
            return
        

    ########## looping até o download concluir 
    def _download(self):
        
        while True:
            cont = 0
            path = Path(self._save)

            for conteudo in path.glob('*'):
                print ("Aguardando termino do download!")
                ext = (conteudo.suffix)
                if ext == '.crdownload' or cont >= 15:
                    time.sleep(5)
                    cont += 1
                else:
                    return  
                    