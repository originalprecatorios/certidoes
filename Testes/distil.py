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
    driver.get('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')  # known url using cloudflare's "under attack mode"
    #time.sleep(6)
    driver.find_element(By.ID,"NI").send_keys("325.044.888-58")
    time.sleep(0.8)
    driver.find_element(By.ID,"validar").click()
    while len(driver.find_elements(By.ID, "FrmSelecao")) < 1:
        print(f"não encontramos")
        time.sleep(0.5)

    url = driver.find_element(By.XPATH,"//*[@id='FrmSelecao']/a[1]").get_attribute("href")
    driver.get(url)

    while len(driver.find_elements(By.ID, "PeriodoInicio")) < 1:
        print(f"não encontramos")
        time.sleep(0.5)

    time.sleep(0.8)
    driver.find_element(By.ID,"validar").click()

    while len(driver.find_elements(By.ID, "resultado")) < 1:
        print(f"não encontramos")
        time.sleep(0.5)

    driver.find_element(By.XPATH,"//*[@id='resultado']/table/tbody/tr[1]/td[7]/a").click()
    time.sleep(4)

