from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from decouple import config
from myclass.captcha import Captcha

import time

if __name__ == '__main__':

    path_download = config('PATH_FILES')+"325.044.888-52"
    options = uc.ChromeOptions()
    options.add_argument('--no-first-run')
    driver = uc.Chrome(options=options, version_main=99)  # version_main allows to specify your chrome version instead of following chrome global version
    #MUDAR A PARSTA DE DOWNLOAD
    params = {
        "behavior": "allow",
        "downloadPath": path_download
    }

    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    try:
        driver.get(config('PAGE_URL_PJE_TRF3'))
        driver.find_element(By.ID,"fPP:dpDec:documentoParte").send_keys("325.044.888-58")
        driver.find_element(By.ID,"fPP:searchProcessos").click()
        #time.sleep(10)
        c = Captcha(config('DATA_SITE_KEY_HCAPTCHA_PJE'),config('PAGE_URL_PJE_TRF3'),'hcaptcha')
        resp = c._resolve()
        #PEGAR O data-hcaptcha-widget-id DO FRAME
        id = driver.find_element(By.XPATH,"//*[@id='fPP:j_id236']/div/iframe").get_attribute("data-hcaptcha-widget-id")
        driver.execute_script(f'document.getElementById("h-captcha-response-{id}").innerHTML="{resp}";')
        driver.execute_script(f'document.getElementById("g-recaptcha-response-{id}").innerHTML="{resp}";')

        time.sleep(1)
        ajax =  driver.find_element(By.ID,"fPP:searchProcessos").get_attribute("onclick")
        separa = ajax.split(";;")
        print(separa[1].replace("return false;",""))
        
        #CALLBACK
        driver.execute_script(separa[1].replace("return false;",""))    

        time.sleep(500)

    except Exception as e:
        print(f"ERRO - _PJE_TRF3 {e}")

