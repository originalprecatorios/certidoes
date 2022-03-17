# CERTIDÃO NEGATIVAS
from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from myclass.captcha import Captcha
from decouple import config
import time

c = Captcha()

def Solver(headless=False,cpf=NULL):
    if cpf != NULL:
        opt = webdriver.ChromeOptions()

        if headless:
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

        driver = webdriver.Chrome(options=opt)
        #driver.implicitly_wait(10)
        #driver.set_page_load_timeout(20)
        
        driver.get(config('PAGE_URL'))
        time.sleep(5)
        driver.find_element(By.ID,"MainContent_txtDocumento").send_keys(f"{cpf}")

        print(f"Meu saldo atual é : {c._saldo()}.")

        wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
        driver.execute_script(wirte_tokon_js)
        time.sleep(3)

        submit = 'MainContent_btnPesquisar'
        driver.find_element(By.ID,submit).click()
        time.sleep(5)
        #MainContent_btnImpressao
        driver.find_element(By.ID,"MainContent_btnImpressao").click()
        time.sleep(100)
    else:
        print("Não consigo trabalhar sem um cpf.")    

if __name__ == '__main__':
    Solver(False,'32504488858')