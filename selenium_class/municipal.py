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

class Municipal:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Municipal')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/municipal/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
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
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_ddlTipoCertidao")))
            select = Select(self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_ddlTipoCertidao'))
            select.select_by_visible_text('Certidão Tributária Mobiliária')
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_ddlTipoDocumento")))
            select = Select(self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_ddlTipoDocumento'))
            select.select_by_visible_text('CPF')
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_txtCPF"))).send_keys(self._data['cpf'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_imgCaptcha")))
           
            cont = 0
            while True:
                if cont <= 5:
                    try:
                        self.solve_cap()
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "btnFecharModalCertidoes")))
                        self._download()
                        self._driver.close()
                        print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                        break
                    except:
                        time.sleep(3)
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_pnlCaptcha")))
                        self._driver.find_element(By.ID,'ctl00_ConteudoPrincipal_pnlCaptcha').find_elements(By.TAG_NAME,'a')[1].click()
                        WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_ddlTipoCertidao")))
                        select = Select(self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_ddlTipoCertidao'))
                        select.select_by_visible_text('Certidão Tributária Mobiliária')
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_ddlTipoDocumento")))
                        select = Select(self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_ddlTipoDocumento'))
                        select.select_by_visible_text('CPF')
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_txtCPF"))).send_keys(self._data['cpf'])
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_imgCaptcha")))
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
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_imgCaptcha")))
            with open(f'{self._capt}captcha.png', 'wb') as file:
                l = self._driver.find_element(By.ID,'ctl00_ConteudoPrincipal_imgCaptcha')
                file.write(l.screenshot_as_png)

            response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            if response is None:
                response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
            #response = ''
            os.system('rm {}'.format(os.path.join(self._capt,'captcha.png')))
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_txtValorCaptcha")))
            self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_txtValorCaptcha').send_keys(response)
            time.sleep(2)
            
            WebDriverWait(self._driver, 2).until(EC.presence_of_element_located((By.ID, "ctl00_ConteudoPrincipal_btnEmitir")))
            self._driver.find_element(By.ID, 'ctl00_ConteudoPrincipal_btnEmitir').click()
     
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