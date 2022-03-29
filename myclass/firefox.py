from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from myclass.gb import Cut
import time, random, os,json,urllib.request

class Firefox:
    def __init__(self,dados):
        self.login = False
        self.path_download = "C:\\"+dados.get('cpf')
        self.dados = dados
        self.tentativas = 0
        self.Erro = 0

        if dados.get('cpf') != "000.000.000-00":
            options = webdriver.FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.download.dir", self.path_download)
            options.set_preference("browser.download.useDownloadDir", True)
            options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
            options.set_preference("browser.helperApps.alwaysAsk.force", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream;application/pdf;")
            options.set_preference("pdfjs.disabled", True)
            self.driver = webdriver.Firefox(options=options)

            #self.driver = webdriver.Firefox('/opt/drivers/chromedriver' , options=opt)
            print("\033[32m"+"Pronto!, Chrome já esta inicializado."+"\033[0;0m")
        else:
            print("Não consigo criar a pasta.")

    def _login_esaj(self):
        self.driver.get("https://esaj.tjsp.jus.br/sajcas/login") 
        #self._existenciaPage("usernameForm") 
        self.driver.find_element(By.ID,"usernameForm").send_keys("60874589134")
        self.driver.find_element(By.ID,"passwordForm").send_keys("bachega@2025")

        self.driver.find_element(By.ID,"pbEntrar").click()
        #ENQUANTO NÂO ACHAR O BOTAO SAIR, ELE VAI FICAR ESPERANDO PQ NÂO CONCLUIU O LOGIN
        while len(self.driver.find_elements(By.CLASS_NAME,"esajLogout")) < 1:
            time.sleep(1)

        self.login = True    

        self.driver.get("https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx")

        time.sleep(1000)
        
