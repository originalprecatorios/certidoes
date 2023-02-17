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
import undetected_chromedriver as uc
import pdfkit
from PIL import Image

class Distribuicao_federal:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha,pInfo,pInstancia,pName):
        print('Robo Distribuicao_federal')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._info = pInfo
        self._instancia = pInstancia
        self._definicao = pName
        
        self._error._getcoll('error')
        self._save = '/opt/certidao/download/distribuicao_federal'
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
        self._driver = uc.Chrome(options=options,version_main=89)
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
            print('login')
            #self._driver.get('https://web.trf3.jus.br/certidao-regional/CertidaoCivelEleitoralCriminal/SolicitarDadosCertidao')

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Tipo")))
            select = Select(self._driver.find_element(By.ID, 'Tipo'))
            select.select_by_value('CIVEL')
            

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "TipoDeDocumento")))
            select = Select(self._driver.find_element(By.ID, 'TipoDeDocumento'))
            select.select_by_value('CPF')
            

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Documento")))
            self._driver.find_element(By.ID,'Documento').send_keys(self._data['cpf'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Nome")))
            self._driver.find_element(By.ID,'Nome').send_keys(self._data['nome'])

            if self._instancia == '1':
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "TipoDeAbrangencia")))
                select = Select(self._driver.find_element(By.ID, 'TipoDeAbrangencia'))
                select.select_by_value('SJSP')
                
            else:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "TipoDeAbrangencia")))
                select = Select(self._driver.find_element(By.ID, 'TipoDeAbrangencia'))
                select.select_by_value('TRF')
                

            response = self._captcha.recaptcha('6Le_CtAZAAAAAEbTeETvetg4zQ7kJI0NH5HNHf1X',self._link)
            #self._driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML = #'"+response+"';")
            self._driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)

            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "submit")))
            self._driver.find_element(By.ID,'submit').click()
           
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "botaoImprimirCertidao")))
            #self._driver.find_element(By.ID,'botaoImprimirCertidao').click()
            cont = 0
            while True:
                if cont >= 3:
                    break
                else:
                    try:
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "botaoImprimirCertidao")))
                        WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ContainerImpressaoCertidao")))
                        break
                    except:
                        time.sleep(2)
                        cont+=1
                        pass
            self._driver.execute_script("document.body.style.zoom='55%'")
            self._driver.execute_script('window.scrollBy(0, 120)')
            self._driver.get_screenshot_as_file(os.path.join(self._save,self._definicao))
            image_1 = Image.open(os.path.join(self._save,self._definicao))
            im_1 = image_1.convert('RGB')
            im_1.save(os.path.join(self._pasta,self._definicao+'.pdf'))
            shutil.rmtree(self._save)
            time.sleep(2)
            '''name = os.path.join(self._save,self._definicao+'.png')
            
            with open(os.path.join(self._save,'page_source.html'), "w") as f:
                f.write(self._driver.page_source)
            try:
                pdfkit.from_file(os.path.join(self._save,'page_source.html'), os.path.join(self._save,f'{self._definicao}.pdf'))
            except:
                pass
            time.sleep(2)
            
            archive_name = os.listdir(self._save)[0]
            shutil.move(f"{self._save}{self._definicao}.pdf", f"{self._pasta}{self._definicao}.pdf")
            shutil.rmtree(self._save)'''
            print('Download concluido para o cpf {}'.format(self._info['cpf']))
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
    
