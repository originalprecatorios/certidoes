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

class Trt15:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/trt15/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
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
        fp.set_preference("pdfjs.disabled", True)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        
        
    
    def login(self):
        try:
            cont = 0
            while True:
                if cont >= 5:
                    break
                WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "eu-cookie-compliance-default-button"))).click()
                iframe = self._driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/article/div/div/p[6]/iframe')
                self._driver.switch_to.frame(iframe)
                WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "certidaoActionForm:j_id23:doctoPesquisa"))).send_keys(self._data['cpf'])
                img = self._driver.find_elements(By.TAG_NAME,'img')[0]
                src = img.get_attribute('src')
                time.sleep(2)
                # download the image
                #urllib.request.urlretrieve(src, os.path.join(self._pasta,'captcha.png'))
                with open(os.path.join(self._pasta,'captcha.png'), 'wb') as file:
                    file.write(self._driver.find_element(By.XPATH,'//*[@id="certidaoActionForm:j_id51"]/div/span[1]/img').screenshot_as_png)
                #response = self._captcha.resolve_normal(os.path.join(self._pasta,'captcha.png'))
                response = ''
                '''if response is None:
                    response = self._captcha.resolve_normal(os.path.join(self._pasta,'captcha.png'))
                
                response = response.replace('=','')
                if '+' in response:
                    soma = int(response.split('+')[0]) + int(response.split('+')[1])
                elif 'x' in response:
                    soma = int(response.split('x')[0]) + int(response.split('x')[1])
                else:
                    soma = int(response)'''


                os.system('rm {}'.format(os.path.join(self._pasta,'captcha.png')))
                element=self._driver.find_element(By.ID,'menuCertidaoActionId')
                element.location_once_scrolled_into_view
                #self._driver.find_elements(By.TAG_NAME,'input')[6].send_keys(str(soma))
                self._driver.find_elements(By.TAG_NAME,'input')[7].click()
                time.sleep(5)
                try:
                    if self._driver.find_element(By.XPATH,'/html/body/div/div/div/div[2]/form/div/div[2]/div[2]/div[4]/div/span[4]').text == 'incorrect response' or self._driver.find_element(By.XPATH,'/html/body/div/div/div/div[2]/form/div/div[2]/div[2]/div[4]/div/span[4]').text == 'Resposta incorreta':
                        cont += 1
                        self._driver.get('https://trt15.jus.br/servicos/certidoes/certidao-eletronica-de-acoes-trabalhistas-ceat')
                        continue
                    else:
                        break
                except:
                    break
            self._driver.find_elements(By.TAG_NAME,'input')[1].click()
            time.sleep(5)
            #self._download()
            self._driver.close()
            print('Download concluido para o cpf {}'.format(self._data['cpf']))


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