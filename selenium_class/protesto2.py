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
import time, os, shutil
import img2pdf
from PIL import Image
import undetected_chromedriver as uc


class Protesto2:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Robo Protesto')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')
        self._save = '/opt/certidao/download/'
        try:
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
            

        
        '''options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
        "download.default_directory": f"{self._save}", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        options.add_argument(f'--user-data-dir={self._save}')
        options.add_argument("start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--no-first-run')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self._driver = webdriver.Chrome(options=options)
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                            'Chrome/85.0.4183.102 Safari/537.36'})
        self._driver.get(self._link)'''

        options = uc.ChromeOptions()
        options.add_experimental_option('prefs', {
        "download.default_directory": f"{self._save}", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        options.add_argument('--no-first-run')
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        # setting profile
        options.user_data_dir = self._save

        # another way to set profile is the below (which takes precedence if both variants are used
        options.add_argument(f'--user-data-dir={self._save}')

        # just some options passing in to skip annoying popups
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        #self._driver = uc.Chrome(options=options)
        #self._driver = uc.Chrome(options=options,version_main=105)
        self._driver = uc.Chrome(options=options,version_main=105)
        try:
            self._driver.set_page_load_timeout(60)
        except:
            pass
        #MUDAR A PARSTA DE DOWNLOAD
        params = {
            "behavior": "allow",
            "downloadPath": self._save
        }

        self._driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
        print('Navegando no site')
        self._driver.get(self._link)
        
        
    
    def login(self):
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "input_cpf_cnpj"))).send_keys(self._data['cpf'])
            response = self._captcha.recaptcha('6LdCOO4dAAAAAEa2FWwvb1wj9V8eItq7c4SPUtUw',self._link)
            #self._driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = '"+response+"';")
            self._driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
            #iframe = self._driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[3]/div[2]/div/div/div/div/iframe')
            #self._driver.switch_to.frame(iframe)
            #ele = self._driver.find_element(By.CSS_SELECTOR,"#recaptcha-token")
            #self._driver.execute_script(f"arguments[0].setAttribute('value','{response}')", ele)
            #self._driver.switch_to.default_content()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "bt-consultar"))).click()
            
            

            self._driver.execute_script("document.getElementById('cookiefirst-root').style.display = 'none'")
            time.sleep(2)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "AbrangenciaNacional"))).click()
            select = Select(self._driver.find_element(By.ID, 'TipoDocumento'))
            select.select_by_visible_text('CPF')
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Documento"))).send_keys(self._data['cpf'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "frmConsulta"))).find_elements(By.TAG_NAME,'input')
            self._driver.execute_script("ValidarConsulta(this)")
            time.sleep(3)
            self._driver.execute_script("document.getElementById('cookiefirst-root').style.display = 'none'")
            time.sleep(2)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "resultado-pesquisa")))
            
            name = os.path.join(self._pasta,'13- CENPROT.png')
            time.sleep(3)
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
            path = Path(self._save)

            for conteudo in path.glob('*'):
                print ("Aguardando termino do download!")
                ext = (conteudo.suffix)
                if ext == '.crdownload' or cont >= 15:
                    time.sleep(5)
                    cont += 1
                else:
                    return 
            return