import requests
from recaptcha.captcha import Solve_Captcha
from bs4 import BeautifulSoup
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import time, os
from recaptcha.captcha import Solve_Captcha
import undetected_chromedriver as uc


sitekey = '6Le9EjMUAAAAAPKi-JVCzXgY_ePjRV9FFVLmWKB_'
captcha = Solve_Captcha()
r = captcha.recaptcha(sitekey,'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf')

capt = '/tmp/captcha/'
if os.path.isdir(f'{capt}'):
  print("O diretório existe!")
else:
  os.makedirs(f'{capt}')
import requests

import requests

url = "https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf"

payload='emitirCrda=emitirCrda&emitirCrda%3AcrdaInputCnpjBase=&emitirCrda%3AcrdaInputCpf=403.154.468-54&g-recaptcha-response=03ANYolqstdCweRJQ4b_yMreUz3PFkDrCnY4KU_jrO7cfi73YebFa3QQI7gPbMnjgy0Vr-DUWL35oSR8vu_qZ4cbY5lf_DtEZj38rfbFjf_AiF8py29A9TFQaiJZe0s460a-HyEVpm-8I21UMDqhFLeNM7hluK4Z4a_C-ydBAqk8icuaoEPQcpRJJ9e55J5NJ54D6v3zmjV5PUlzjE1FJpn4nm6K9coZXWyuaM_dPXo9s6cByC3ckvp6Lqc68UDGVUX7MKVyoYDiGXII7B-8yNRvaBMcfJmbXhvRSRZrUFAdxVkwk0qE4lhD_6lpqLnRzhJvUMJ0mwMpyUCdWk6m6n-tQR4QSJEzPATnNumtTkbxTBMoNapP7SaNw&emitirCrda%3Aj_id95=Emitir&javax.faces.ViewState=j_id2'
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://www.dividaativa.pge.sp.gov.br',
  'DNT': '1',
  'Connection': 'keep-alive',
  'Referer': 'https://www.dividaativa.pge.sp.gov.br/sc/pages/crda/emitirCrda.jsf;jsessionid=524AA237088F50590D560C87068D972F.395016-sc-01',
  'Cookie': 'JSESSIONID=524AA237088F50590D560C87068D972F.395016-sc-01',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
