from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import time, os
from recaptcha.captcha import Solve_Captcha
import undetected_chromedriver as uc

class Federal:

    def __init__(self,pData,pLink,pMongo, pError,pR):
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._error._getcoll('error')

        self._pasta = '/tmp/pdf/federal/{}'.format(self._data['cpf'].replace('.','').replace('-',''))
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
        self._driver.delete_all_cookies()
        self._driver.add_cookie({'name': 'ASP.NET_SessionId', 'value': '0v2vx102maa4hqaq4i45mxcf', 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'Lax'})
        self._driver.add_cookie({'name': 'BIGipServerPOOL_SERVICO_RECEITA', 'value': '1558680737.47873.0000', 'path': '/', 'domain': 'solucoes.receita.fazenda.gov.br', 'secure': True, 'httpOnly': True, 'sameSite': 'None'})
        self._driver.get('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir/EmProcessamento?Ni=28933622810')
        time.sleep(2)
        '''

        self._options = uc.ChromeOptions()
        time.sleep(2)
        self._options.add_argument("--start-maximized")
        self._driver = uc.Chrome(options=self._options)

        self._driver.get(self._link)
        time.sleep(2)
        '''
        
        
    
    def login(self):
        try:
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(self._data['cpf'])
            sitekey = '4a65992d-58fc-4812-8b87-789f7e7c4c4b'
            captcha = Solve_Captcha()
            r = captcha.resolve_hcaptcha(sitekey,'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')
            self._driver.execute_script(f"document.getElementsByName('h-captcha-response').value = '{r}';")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "validar"))).click()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "FrmSelecao"))).find_elements(By.TAG_NAME,'a')[1].click()
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "rfb-main-container")))
            self._download()
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