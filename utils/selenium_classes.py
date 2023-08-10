from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from utils.firefox_download import TEXTO
from decouple import config
import undetected_chromedriver as uc
import time, os

LOCATORS = {
        "ID": By.ID,
        "CLASS_NAME": By.CLASS_NAME,
        "NAME": By.NAME,
        "TAG_NAME": By.TAG_NAME,
        "XPATH": By.XPATH,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
}

class Selenium_classes:
    def __init__(self,pPath=None):
        self.print_colored("Executando a classe Selenium", "blue")
        if pPath is not None:
            self.create_folder(pPath)
        
    def firefox(self,pLink,pSave=None,pOpen=True):
        self.print_colored("Executando navegador FireFox", "blue")
        options = Options()
        #options = webdriver.FirefoxProfile()
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        if pSave is not None:
            options.set_preference("browser.download.dir", pSave)
        options.set_preference(TEXTO[0], TEXTO[1])
        options.set_preference("pdfjs.disabled", True)
        if pOpen is False:
            options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)
        self._driver.get(pLink)
        time.sleep(2)
    
    def accept_cookie(self):
        try:
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "eu-cookie-compliance-default-button"))).click()
        except:
            pass
    
    def download_img(self,pPath):
        img = self._driver.find_elements(By.TAG_NAME,'img')[0]
        
        time.sleep(2)
        # download the image
        #urllib.request.urlretrieve(src, os.path.join(self._pasta,'captcha.png'))
        with open(os.path.join(pPath,'captcha.png'), 'wb') as file:
            file.write(self._driver.find_element(By.XPATH,'/html/body/img').screenshot_as_png)
    
    def chrome(self,pLink,pSave=None):
        from selenium.webdriver.chrome.options import Options
        self.print_colored("Executando navegador Chrome ", "blue")
        options = Options()
        options.add_argument('--no-first-run')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        if pSave is not None:
            options.add_experimental_option("prefs", {
                "download.default_directory": pSave,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
        self._driver = webdriver.Chrome(options=options)
        self._driver.get(pLink)
        time.sleep(2)
    
    def u_chrome(self,pLink,pSave):
        self.print_colored("Executando navegador Undetected Chrome ", "blue")
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        if pSave is not None:
            options.add_experimental_option('prefs', {
            "download.default_directory": f"{pSave}", #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
            })
        self._driver = uc.Chrome(options=options,version_main=int(config('VERSION')))
        try:
            self._driver.set_page_load_timeout(60)
        except:
            pass
        if pSave is not None:
            #MUDAR A PARSTA DE DOWNLOAD
            params = {
                "behavior": "allow",
                "downloadPath": pSave
            }

            self._driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
            self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                        'Chrome/85.0.4183.102 Safari/537.36'})
        self._driver.get(pLink)
        time.sleep(2)
    
    def navegation(self,pLink):
        self._driver.get(pLink)
    
    def close_driver(self):
        self.print_colored("Fechando Navegador", "blue")
        self._driver.close()
    
    # Cria uma pasta conforme passado no parametro
    def create_folder(self,pPath):
        self.print_colored("Criando pasta", "blue")
        if os.path.isdir(f'{pPath}'):
            self.print_colored("O diretório existe!", "red")
        else:
            os.makedirs(f'{pPath}')
            self.print_colored("Diretório Criado!", "green")

    # Cria um print com cor
    def print_colored(self, text, color):
        colors = {
            'blue': '\033[94m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'green': '\033[92m'
        }

        end_color = '\033[0m'

        if color.lower() in colors:
            colored_text = colors[color.lower()] + text + end_color
            print(colored_text)
        else:
            print("A cor selecionada não existe")
    
    def locators(self,pType,pElement):
        if pType in LOCATORS:
            return (LOCATORS[pType], pElement)
        else: 
            return self.print_colored("Tipo de localizador não suportado.", "red")
    
    def wait_element(self,pType,pElement,pAll=False):
        self.print_colored("Aguardando elemento existente na tela", "blue")
        locator = self.locators(pType,pElement)
        if pAll is False:
            return WebDriverWait(self._driver, 5).until(EC.presence_of_element_located(locator))
        else:
            return WebDriverWait(self._driver, 5).until(EC.presence_of_all_elements_located(locator))
    
    def select(self,pType,pElement,pData):
        self.print_colored("Selecionando elemento", "blue")
        self.wait_element(pType, pElement)
        locator = self.locators(pType,pElement)
        select = Select(self._driver.find_element(*locator))
        return select.select_by_value(pData)
    
    def element(self,pType,pElement,pAll=False):
        self.print_colored("Executando ação no elemento", "blue")
        self.wait_element(pType, pElement)
        locator = self.locators(pType,pElement)
        if pAll is False:
            return self._driver.find_element(*locator)
        else:
            return self._driver.find_elements(*locator)
    
    def element_alert(self,pAceppt=False):
        self.print_colored("Verificando alertas", "blue")
        alert = self._driver.switch_to.alert
        if pAceppt is False:
            alert.accept()
        else:
            alert.dismiss()
    
    def new_window(self,pLink,pPage=1):
        self.print_colored("Abrindo nova aba", "blue")
        self._driver.execute_script(f"window.open('{pLink}', '_blank')")
        self._driver.switch_to.window(self._driver.window_handles[pPage])
    
    def close_window(self,pPage=0):
        self.print_colored("Fechando nova aba", "blue")
        self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[pPage])
    
    def select_iframe(self,pType,pElement):
        self.print_colored("Selecionando elemento iframe", "blue")
        locator = self.locators(pType,pElement)
        iframe = self._driver.find_element(*locator)
        self._driver.switch_to.frame(iframe)
    
    def close_iframe(self):
        self.print_colored("Fechando elemento iframe", "blue")
        self._driver.switch_to.default_content()

    def screen(self,pName):
        self.print_colored("Tirando um print da tela", "blue")
        self._driver.get_full_page_screenshot_as_file(pName)
    
    def cookies(self):
        self.print_colored("Pegando os cookies de sessão", "blue")
        return self._driver.get_cookies()