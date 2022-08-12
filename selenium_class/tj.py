from importlib.resources import path
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
import img2pdf
from PIL import Image


class Tj:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Tj')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/tj/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')

        
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
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "cbPesquisa")))
            select = Select(self._driver.find_element(By.ID, 'cbPesquisa'))
            select.select_by_visible_text('Documento da Parte')
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "campo_DOCPARTE"))).send_keys(self._data['cpf'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "botaoConsultarProcessos"))).click()
            time.sleep(5)

            name = os.path.join(self._pasta,self._data['cpf'].replace('-','').replace('.','')+'.png')
            
            self._driver.get_full_page_screenshot_as_file('{}'.format(name))
            self.convert(name)
            print('Download concluido para o cpf {}'.format(self._data['cpf']))
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