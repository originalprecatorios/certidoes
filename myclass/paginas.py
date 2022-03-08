#from lib2to3.pgen2 import driver
from turtle import width
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from myclass.captcha import Captcha
from myclass.gb import Cut
from decouple import config
#import urllib.request
import time, random, os

class Paginas:
    def __init__(self,cpf='000'):
        if cpf != "000":
            opt = webdriver.ChromeOptions()

            if config('HEADLESS') == True:
                opt.add_argument("--headless")

            opt.add_argument("--disable-xss-auditor")
            opt.add_argument("--disable-web-security")
            opt.add_argument("--allow-running-insecure-content")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-setuid-sandbox")
            opt.add_argument("--disable-webgl")
            opt.add_argument("--disable-popup-blocking")

            opt.add_experimental_option( "prefs", {
                                                    'profile.default_content_settings.popups': 0,
                                                    'download.prompt_for_download' : False,
                                                    'download.default_directory': f'C:\{cpf}',
                                                    'profile.default_content_setting_values.automatic_downloads':1
                                                })

            self.driver = webdriver.Chrome(options=opt)
            #driver.implicitly_wait(10)
            #driver.set_page_load_timeout(20)
            print("Pronto!, Chrome já esta inicializado.")
        else:
            print("Não consigo criar a pasta.")
    def _login_esaj(self):
        self.driver.get(config('ESAJ_PAGE_LOGIN')) 
        self._existenciaPage("usernameForm") 
        self.driver.find_element(By.ID,"usernameForm").send_keys(f"{config('ESAJ_USER')}")
        self.driver.find_element(By.ID,"passwordForm").send_keys(f"{config('ESAJ_PASS')}")

        self.driver.find_element(By.ID,"pbEntrar").click()
        #ENQUANTO NÂO ACHAR O BOTAO SAIR, ELE VAI FICAR ESPERANDO PQ NÂO CONCLUIU O LOGIN
        while len(self.driver.find_elements(By.CLASS_NAME,"esajLogout")) < 1:
            time.sleep(1)


    def _existenciaPage(self,id):
        while True:
                if self.driver.page_source.find(f"{id}"):
                    print(f"encontrado na pagina {id}")
                    break
                else:
                    print(f"não encontramos {id} na pagina")
                    time.sleep(0.5)
                    pass

    def _select(self,id,value):
        while True:
                try:
                    select = Select(self.driver.find_element(By.ID, f"{id}"))
                    select.select_by_value(f'{value}')
                    break
                except:
                    time.sleep(2)
                    pass

    def _CND_Estadual (self,cpf='000'):
        if cpf != "000":
            
            self.driver.get(config('PAGE_URL'))
            #VERIFICAR SE A PAGINA JA ESTA CARREGADA
            self._existenciaPage("MainContent_txtDocumento")

            self.driver.find_element(By.ID,"MainContent_txtDocumento").send_keys(f"{cpf}")

            c = Captcha(config('DATA_SITE_KEY'),config('PAGE_URL'))

            #print(f"Meu saldo atual é : {c._saldo()}.")

            wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
            self.driver.execute_script(wirte_tokon_js)
            time.sleep(1)

            self.driver.find_element(By.ID,"MainContent_btnPesquisar").click()
            time.sleep(0.5)

            #VOU VERIFICAR SE EXISTE O BOTÂO DE IMPRIMIR NA TELA, SE SIM CLICK NELE
            self._existenciaPage("MainContent_btnImpressao")   

            self.driver.find_element(By.ID,"MainContent_btnImpressao").click()

            del c
            time.sleep(4)
        else:
            print("Ausencia de parametros para consulta.")

    def _CND_Municipal(self,cpf='000'):
        if cpf != "000":
            self.driver.get(config('PAGE_URL_MUN'))
            self._select('ctl00_ConteudoPrincipal_ddlTipoCertidao','1')
            self._select('ctl00_ConteudoPrincipal_ddlTipoDocumento','CPF')
            time.sleep(0.8)
            self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_txtCPF").send_keys(f"{cpf}")

            namefile = random.randrange(99999)
            self.driver.save_screenshot("page_"+str(namefile)+".png")
            a = Cut()
            #CROP ARQUIVO DE PRINT TELA, NOME DO ARQUIVO QUANDO CORTADO
            test = a.crop("page_"+str(namefile)+".png","crop_"+str(namefile))

            c = Captcha(test,"")
            
            self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_txtValorCaptcha").send_keys(f"{c._resolve_img()}")
            time.sleep(0.5)
            self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_btnEmitir").click()
            #APAGAR OS ARQUIVOS GERADOS
            os.remove("page_"+str(namefile)+".png")
            os.remove("crop_"+str(namefile)+".png")

            del c
                
            time.sleep(4)    
        else:
            print("Ausencia de parametros para consulta.")

    def _CND_Contribuinte(self,cpf='000'):
        if cpf != "000":
            self.driver.get(config('PAGE_URL_CONTRIBUINTE'))
            self._existenciaPage("emitirCrda:crdaInputCpf")
            self.driver.find_element(By.ID,"emitirCrda:crdaInputCpf").send_keys(f"{cpf}")
            c = Captcha(config('DATA_SITE_KEY_CONTRIBUINTE'),config('PAGE_URL_CONTRIBUINTE'))
            #print(f"Meu saldo atual é : {c._saldo()}.")
            wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
            self.driver.execute_script(wirte_tokon_js)
            time.sleep(3)
            self.driver.find_element(By.XPATH,"//*[@id='emitirCrda:j_id136_body']/div[2]/input[2]").click()

            del c

            time.sleep(4)
        else:
            print("Ausencia de parametros para consulta.")            

    def _CND_Federal(self,cpf='000'):
        if cpf != "000":
            self.driver.get(config('PAGE_URL_FEDERAL'))
            self._existenciaPage("NI")
            self.driver.find_element(By.ID,"NI").send_keys(f"{cpf}")
            time.sleep(1)
            self.driver.find_element(By.ID,"validar").click()
            time.sleep(5)

            if self.driver.page_source.find("Emissão de nova certidão"):
                self.driver.find_element(By.XPATH,"//*[@id='FrmSelecao']/a[2]").click()
                time.sleep(5)

        else:
            print("Ausencia de parametros para consulta.")    
