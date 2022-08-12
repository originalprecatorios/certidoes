from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import os, time


class Estadual:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Estadual')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/estadual/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')


        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self._pasta)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        
        
    
    def login(self):
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "MainContent_cpfradio"))).click()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "MainContent_txtDocumento"))).send_keys(self._data['cpf'])

            response = self._captcha.recaptcha('6LdoPeUUAAAAAIC5yvhe7oc9h4_qf8_Vmq0xd9GU',self._link)
            self._driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = '"+response+"';")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "MainContent_btnPesquisar"))).click()

            try:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "MainContent_PnlMensagemUsuario")))
                self._driver.close()
                return False
            except:
                return True


        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'estadual',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            return
    
    def download_document(self):
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "MainContent_btnImpressao"))).click()
            self._download()
            self._driver.close()
            print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
        except:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'estadual',
                    'funcao' : 'erro na função download_document',
            }
            self._error.addData(err)
        

    ########## looping até o download concluir 
    def _download(self):
        
        while True:
            cont = 0
            path = Path(self._pasta)

            for conteudo in path.glob('*'):
                print ("Aguardando termino do download!")
                ext = (conteudo.suffix)
                if ext == '.crdownload' or cont >= 15:
                    time.sleep(5)
                    cont += 1
                else:
                    return  