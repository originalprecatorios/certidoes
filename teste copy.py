from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from speech_recognition import AudioFile, Recognizer
from pydub import AudioSegment
from requests import get
from time import sleep
import pyautogui
import json
from selenium.webdriver.common.by import By


#PROXY = "13.251.26.136:3128"
options = Options()
options.add_argument("--window-size=2560,1440")
options.add_argument("--incognito")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument("--disable-extensions")
#options.add_argument('--proxy-server=%s' % PROXY)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('prefs', {
        "download.default_directory": "PASTA ONDE VAI SALVAR", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
options.add_argument(f'--user-data-dir=PASTA ONDE VAI SALVAR')


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response



caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = Chrome(options=options, desired_capabilities=caps)
URL = 'https://www10.fazenda.sp.gov.br/CertidaoNegativaDeb/Pages/EmissaoCertidaoNegativa.aspx'
driver.get(URL)
sleep(2)
driver.find_element(By.NAME,'ctl00$MainContent$txtDocumento').send_keys('000.000.000-00')

pyautogui.click(736,533)
sleep(3)
pyautogui.click(385,729)
sleep(3)
driver.switch_to.default_content()
iframe = driver.find_elements(By.TAG_NAME,'iframe')[-1]
driver.switch_to.frame(iframe)
lastaudio = driver.find_element(By.CLASS_NAME,'rc-audiochallenge-tdownload-link').get_attribute('href')


with open('1.mpeg', 'wb') as f:
    f.write(get(lastaudio).content)
    
sound = AudioSegment.from_mp3("1.mpeg")
sound.export("transcript.wav", format="wav")
                  
r = Recognizer()

with AudioFile('transcript.wav') as source:
        audio = r.record(source)
        transcript =  r.recognize_google(audio)
        print("Transcription: " + transcript)


i = driver.find_elements(By.TAG_NAME,'input')[1].send_keys(transcript + Keys.ENTER)

sleep(5)
driver.switch_to.default_content()
driver.find_element(By.NAME,'ctl00$MainContent$btnPesquisar').click()
sleep(2)
driver.find_element(By.ID,'MainContent_btnImpressao').click()
print('Download Concluido')