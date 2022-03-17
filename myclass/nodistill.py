from myclass.captcha import Captcha
from decouple import config
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import time

class Nodistill:

    def __init__(self,dados):
        self.path_download = config('PATH_FILES')+dados.get('cpf')
        self.dados = dados

        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument("--window-size=2560,1440")
        self.driver = uc.Chrome(options=options, version_main=99)
        #MUDAR A PARSTA DE DOWNLOAD
        params = {
            "behavior": "allow",
            "downloadPath": self.path_download
        }

        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    def _existenciaPage(self,id):
        while len(self.driver.find_elements(By.ID, id)) < 1:
            print(f"não encontramos {id} na pagina")
            time.sleep(0.5)    

    def _pje_trf3(self):
        self.driver.get(config('PAGE_URL_PJE_TRF3'))
        self.driver.find_element(By.ID,"fPP:dpDec:documentoParte").send_keys(self.dados.get('cpf'))
        self.driver.find_element(By.ID,"fPP:searchProcessos").click()

        c = Captcha(config('DATA_SITE_KEY_HCAPTCHA_PJE'),config('PAGE_URL_PJE_TRF3'),'hcaptcha')
        resp = c._resolve()
        #PEGAR O data-hcaptcha-widget-id DO FRAME
        id = self.driver.find_element(By.XPATH,"//*[@id='fPP:j_id236']/div/iframe").get_attribute("data-hcaptcha-widget-id")
        #print(id)
        #self.driver.execute_script(f'document.getElementById("g-recaptcha-response-{id}").innerHTML="{resp}";')
        self.driver.execute_script(f'document.getElementById("h-captcha-response-{id}").innerHTML="{resp}";')
        #CALLBACK
        self.driver.execute_script("A4J.AJAX.Submit('fPP',event,{'similarityGroupingId':'fPP:searchProcessos','parameters':{'fPP:searchProcessos':'fPP:searchProcessos'} } )")    
        time.sleep(4)

    def _CND_Federal(self):
        self.driver.get(config('PAGE_URL_FEDERAL'))
        self.driver.find_element(By.ID,"NI").send_keys(self.dados.get('cpf'))
        time.sleep(0.8)
        self.driver.find_element(By.ID,"validar").click()
        self._existenciaPage("FrmSelecao")

        url = self.driver.find_element(By.XPATH,"//*[@id='FrmSelecao']/a[1]").get_attribute("href")
        self.driver.get(url)

        self._existenciaPage("PeriodoInicio")

        time.sleep(0.8)
        self.driver.find_element(By.ID,"validar").click()

        self._existenciaPage("resultado")

        self.driver.find_element(By.XPATH,"//*[@id='resultado']/table/tbody/tr[1]/td[7]/a").click()
        time.sleep(4)

    def _trf3_jus(self):
        self.driver.get(config('PAGE_URL_TRF3_JUS'))
        self._existenciaPage("Nome")
        self.driver.find_element(By.ID,"abrangenciaSJSP").click()
        self.driver.find_element(By.ID,"Nome").send_keys(self.dados.get('nome'))
        time.sleep(0.8)
        self.driver.execute_script(f"document.getElementById('CpfCnpj').value = '{self.dados.get('cpf')}'")
        time.sleep(0.8)
        self.driver.find_element(By.ID,"BtGeraCerticao").click()

        while True:
            if self.driver.pag_source.find("Gerar PDF") > -1:
                print("O cara existe")
                self.driver.find_element(By.XPATH,"//*[@id='frm']/p/a").click()
                break
            else:
                print("Não existe ainda")
                time.sleep(2)
                pass
        time.sleep(4)    

