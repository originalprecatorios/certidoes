from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pathlib import Path
import time, os

class Trabalhista:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha,pInfo,pInstancia):
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._info = pInfo
        self._instancia = pInstancia
        self._error._getcoll('error')

        self._save = '/opt/certidao/download/'
        self._pasta = '/opt/certidao/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
            os.makedirs(f'{self._save}')

        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self._save)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
        fp.set_preference("pdfjs.disabled", True)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        
        
    
    def login(self):
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "TipoCertidao4"))).click()
            if self._instancia == '1':
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "abrangenciaSJSP"))).click()
            else:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "abrangenciaTRF"))).click()        
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Nome"))).send_keys(self._info['nome'].strip())
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "PessoaFisicaComCpf"))).click()
            self._driver.execute_script(f"document.getElementById('CpfCnpj').value = '{self._info['cpf']}'")
            self._driver.delete_all_cookies()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "BtGeraCerticao"))).click()
            cont = 0
            while True:
                if cont <= 5:
                    try:
                        WebDriverWait(self._driver, 20).until(EC.presence_of_element_located((By.ID, "botaoImprimir")))
                        break
                    except:
                        cont += 1
                        time.sleep(3)
                        continue

                else:
                    break
            self._driver.delete_all_cookies()
            self._link_download = WebDriverWait(self._driver, 20).until(EC.presence_of_element_located((By.ID, "frm"))).find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
            WebDriverWait(self._driver, 20).until(EC.presence_of_element_located((By.ID, "frm"))).find_elements(By.TAG_NAME,'a')[0].click()
            #self._driver.delete_all_cookies()
            #self._driver.get(self._link_download)
            self._download()
            print('Download concluido para o cpf {}'.format(self._info['cpf']))
            self._driver.close()

        except Exception as e:
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            return

    
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