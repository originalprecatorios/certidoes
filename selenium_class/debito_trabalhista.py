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

class Debito_trabalhista:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Debito_trabalhista')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/debito_trabalhista/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
        
        self._capt = '/tmp/captcha/'
        if os.path.isdir(f'{self._capt}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._capt}')

        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self._pasta)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
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
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "post-added"))).find_element(By.TAG_NAME,'a').click()
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "layout-column_column-2")))
            time.sleep(2)
            iframe = self._driver.find_element(By.ID,'layout-column_column-2').find_elements(By.CLASS_NAME,"journal-content-article")[1].find_element(By.TAG_NAME,'iframe')
            self._driver.execute_script("window.scrollTo(0, 300)")
            time.sleep(1)
            self._driver.switch_to.frame(iframe)         
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "botao")))
            self._driver.find_elements(By.CLASS_NAME,"botao")[0].click()
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "gerarCertidaoForm:cpfCnpj"))).send_keys(self._data['cpf'])
            
            cont = 0
            while True:
                if cont <= 5:
                    try:
                        self.solve_cap()
                        if WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "gerarCertidaoForm:mensagemSucesso"))).text != '' :
                            self._download()
                            self._driver.close()
                            print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                            break
                        else:
                            time.sleep(3)
                            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "botao")))
                            self._driver.find_elements(By.CLASS_NAME,"botao")[0].click()
                            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "gerarCertidaoForm:cpfCnpj"))).send_keys(self._data['cpf'])
                            cont += 1
                            continue
                    except:
                        time.sleep(3)
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "botao")))
                        self._driver.find_elements(By.CLASS_NAME,"botao")[0].click()
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "gerarCertidaoForm:cpfCnpj"))).send_keys(self._data['cpf'])
                        cont += 1
                        continue
                else:
                    break

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
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idImgBase64")))
            time.sleep(2)
            with open(f'{self._capt}captcha.png', 'wb') as file:
                l = self._driver.find_element(By.ID,'idImgBase64')
                file.write(l.screenshot_as_png)
            time.sleep(1)
            self._driver.switch_to.default_content()
            iframe = self._driver.find_element(By.ID,'layout-column_column-2').find_elements(By.CLASS_NAME,"journal-content-article")[1].find_element(By.TAG_NAME,'iframe')
            self._driver.execute_script("window.scrollTo(0, 300)")
            time.sleep(1)
            self._driver.switch_to.frame(iframe)         
            response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            if response is None:
                response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            #response = ''
            time.sleep(1)
            os.system('rm {}'.format(os.path.join(self._capt,'captcha.png')))
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "idCaptcha")))
            self._driver.find_element(By.ID, 'idCaptcha').send_keys(response)
            time.sleep(2)
            
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "gerarCertidaoForm:btnEmitirCertidao")))
            self._driver.find_element(By.ID, 'gerarCertidaoForm:btnEmitirCertidao').click()
     
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
            path = Path(self._pasta)

            for conteudo in path.glob('*'):
                print ("Aguardando termino do download!")
                ext = (conteudo.suffix)
                if ext == '.crdownload' or cont >= 15:
                    time.sleep(5)
                    cont += 1
                else:
                    return  