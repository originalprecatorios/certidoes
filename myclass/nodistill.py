from myclass.captcha import Captcha
from decouple import config
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import time

class Nodistill:

    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        self.driver = uc.Chrome(options=options, version_main=99)

    def _pje_trf3(self,cpf):
        self.driver.get(config('PAGE_URL_PJE_TRF3'))
        self.driver.find_element(By.ID,"fPP:dpDec:documentoParte").send_keys(cpf)
        self.driver.find_element(By.ID,"fPP:searchProcessos").click()

        c = Captcha(config('DATA_SITE_KEY_HCAPTCHA_PJE'),config('PAGE_URL_PJE_TRF3'),'hcaptcha')
        resp = c._resolve()
        #PEGAR O data-hcaptcha-widget-id DO FRAME
        id = self.driver.find_element(By.XPATH,"//*[@id='fPP:j_id236']/div/iframe").get_attribute("data-hcaptcha-widget-id")
        #print(id)
        self.driver.execute_script(f'document.getElementById("g-recaptcha-response-{id}").innerHTML="{resp}";')
        self.driver.execute_script(f'document.getElementById("h-captcha-response-{id}").innerHTML="{resp}";')
        #CALLBACK
        self.driver.execute_script("A4J.AJAX.Submit('fPP',event,{'similarityGroupingId':'fPP:searchProcessos','parameters':{'fPP:searchProcessos':'fPP:searchProcessos'} } )")
        

        time.sleep(1000)
