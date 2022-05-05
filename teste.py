# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver.v2 as uc
# import time

# options = uc.ChromeOptions()
# options.add_argument('--no-first-run')
# options.add_argument("--window-size=2560,1440")
# options.add_argument('--no-sandbox')
# driver = uc.Chrome(options=options, version_main=89)
# #MUDAR A PARSTA DE DOWNLOAD
# params = {
# 	"behavior": "allow",
#         "downloadPath": "/opt"
# }

# driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

# driver.get("https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir")
# wait = WebDriverWait(driver, 120)
# wait.until(EC.presence_of_element_located((By.ID, "NI")))
# driver.find_element(By.ID,"NI").send_keys("325.044.888-58")
# driver.find_element(By.ID,"validar").click()
# wait.until(EC.presence_of_element_located((By.ID,"FrmSelecao")))

# driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div/div/div/div/form/a[1]").click()
# wait.until(EC.presence_of_element_located((By.ID,"frmInfParam")))
# driver.find_element(By.ID,"validar").click()

# wait.until(EC.presence_of_element_located((By.CLASS_NAME,"fileDownloadAlerta")))
# driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div/div/div/div/div[3]/table/tbody/tr[1]/td[7]/a").click()


# time.sleep(20)


import cv2
import pytesseract
config = ('-l eng --oem 1 --psm 3')
img_cv = cv2.imread('/home/rafael/Original/certidoes/crop_3753547.png')

text = pytesseract.image_to_string(img_cv, config=config)
print(text)


