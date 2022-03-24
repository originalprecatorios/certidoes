from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from decouple import config

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

    arq = open(config('PATH_FILES')+"022.090.028-00/resumo.txt","a")
    arq.write("Teste \n")
    arq.close()
                
    driver.get('https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx')  # known url using cloudflare's "under attack mode"
    #time.sleep(6)
    driver.find_element(By.ID,"MainContent_txtDocumento").send_keys("325.044.888-58")

    frame = driver.find_element(By.XPATH,"//*[@id='ReCaptchContainer']/div/div/iframe") 
    driver.switch_to.frame(frame)
    driver.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click()

    time.sleep(100)

