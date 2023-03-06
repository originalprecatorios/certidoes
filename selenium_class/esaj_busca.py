from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pathlib import Path
from decouple import config
import time, os,shutil
from PIL import Image
import img2pdf

class Esaj_busca:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha,pName):
        print('Robo Esaj_busca')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._definicao = pName
        self._error._getcoll('error')
        self._save = '/opt/certidao/download/esaj_busca'
        try:
            if os.path.isdir(f'{self._save}') is False:
                os.makedirs(f'{self._save}')
            else:
                shutil.rmtree(self._save)
                os.makedirs(f'{self._save}')
        except:
            pass
        self._pasta = self._data['path']
        #self._pasta = '/opt/certidao/{}/'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')
            
    
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("pdfjs.disabled", True)
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
        
        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            
            return
    
    def get_data(self,pSelect):
        try:    
            self._driver.get(config('PAGE_URL_ESAJ_B_NOME_CPF'))
            time.sleep(2)
            if pSelect == "NOME":
                ValueSelect = "NMPARTE"
                ValueInput = self._data['nome']
            else:
                ValueSelect = "DOCPARTE"  
                ValueInput = self._data['cpf']

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "cbPesquisa")))
            select = Select(self._driver.find_element(By.ID, 'cbPesquisa'))
            select.select_by_value(f'{ValueSelect}')
            time.sleep(2)
            self._driver.find_element(By.ID, f"campo_{ValueSelect}").send_keys(ValueInput)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "botaoConsultarProcessos")))
            self._driver.find_element(By.ID,"botaoConsultarProcessos").click()
            time.sleep(4)
            name = os.path.join(self._pasta,self._definicao+'.png')
            time.sleep(3)
            self._driver.get_full_page_screenshot_as_file('{}'.format(name))
            self.convert(name)
            print('Download concluido para o cpf {}'.format(self._data['cpf']))
            self._driver.close()
            time.sleep(6)

        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            
            return
    
    def convert(self,pName):
        # storing image path
        img_path = pName
        
        # storing pdf path
        pdf_path = pName.replace('png','pdf')
        
        # opening image
        image = Image.open(img_path)
        
        # converting into chunks using img2pdf
        pdf_bytes = img2pdf.convert(image.filename)
        
        # opening or creating pdf file
        file = open(pdf_path, "wb")
        
        # writing pdf files with chunks
        file.write(pdf_bytes)
        
        # closing image file
        image.close()
        
        # closing pdf file
        file.close()
        
        os.remove(img_path)
        # output
        print("Successfully made pdf file")