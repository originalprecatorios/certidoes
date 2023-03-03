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
from decouple import config
from selenium.webdriver.common.action_chains import ActionChains


class Federal:

    def __init__(self,pData,pLink,pMongo, pError,pCnpj):
        print('Robo Federal')
        self._data = pData
        self._link = pLink
        self._cnpj = pCnpj
        self._bdMongo = pMongo
        self._error = pError
        
        self._error._getcoll('error')
        self._save = '/opt/certidao/download/federal'
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
        options.add_argument('--no-first-run')
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        options.add_experimental_option('prefs', {
        "download.default_directory": f"{self._save}", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        #self._driver = uc.Chrome(options=options,version_main=105)
        self._driver = uc.Chrome(options=options,version_main=int(config('VERSION')))
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
        time.sleep(1)
        print('Navegando no site')
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                     'Chrome/85.0.4183.102 Safari/537.36'})
        self._driver.get(self._link)
        
        
    
    def login(self):
        print('login')
        try:
            time.sleep(3)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(self._cnpj)
            time.sleep(2)
            button_element = self._driver.find_element(By.ID, "validar")
            action = ActionChains(self._driver)
            action.move_to_element(button_element).perform()
            action.click(button_element).perform()
            #WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "validar"))).click()
            time.sleep(2)
            #self._driver.execute_script("window.stop();")
            
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "FrmSelecao")))
            self._driver.find_element(By.ID,"FrmSelecao").find_elements(By.TAG_NAME,"a")[1].click()
            time.sleep(10)
            try:
                WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
            except:
                self._driver.refresh()
                pass
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
            try:
                self.get_download()
            except:
                self._driver.refresh()
                self.get_download()     
            
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
            self._driver.close()
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
            return
    
    def get_download(self):
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
        if self._driver.find_element(By.ID,'main').text.find('A certidão foi emitida com sucesso') >= 0:
            time.sleep(2)
            self._download()
            archive_name = os.listdir(self._save)[0]
            shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}4- CND FEDERAL.pdf")
            print('Download concluido para o cpf {}'.format(self._cnpj))
        else:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "rfb-main-container")))
            self._driver.find_element(By.ID,"rfb-main-container").find_element(By.TAG_NAME,"a").click()
            time.sleep(2)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(self._cnpj)
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "validar"))).click()
            time.sleep(3)
            self._download()
            if len(os.listdir(self._save)) > 1:
                for l in os.listdir(self._save):
                    if l.find('.pdf') >= 0:
                        archive_name = l
                        break
            else:   
                archive_name = os.listdir(self._save)[0]
            shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}4- CND FEDERAL.pdf")
            shutil.rmtree(self._save)
            print('Download concluido para o cpf {}'.format(self._cnpj))
                    