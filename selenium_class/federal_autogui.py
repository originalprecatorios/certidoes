import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from pathlib import Path
import time, os, shutil
import undetected_chromedriver as uc
from decouple import config


class Federal:

    def __init__(self,pData,pMongo, pError,pCnpj):
        print('Robo Federal')
        self._data = pData
        self._cnpj = pCnpj
        self._bdMongo = pMongo
        self._error = pError
        
        self._error._getcoll('error')
        self._save = os.path.join(os.path.expanduser("~"), "Downloads")
        self._pasta = self._data['path']
        if os.path.isdir(f'{self._pasta}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{self._pasta}')     
        
    
    def login(self):
        print('login')
        #os.system('firefox')
        #time.sleep(5)
        #pyautogui.write('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')
        #pyautogui.hotkey('enter')
        time.sleep(5)
        #pyautogui.hotkey('ctrl','t')
        #pyautogui.write('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PF/Emitir')
        #time.sleep(10)
        #pyautogui.hotkey('enter')
        pyautogui.click(278,603)
        time.sleep(2)
        pyautogui.hotkey('tab')
        pyautogui.write(self._data['cpf'].replace('.','').replace('-',''))
        pyautogui.hotkey('enter')
        time.sleep(5)
        pyautogui.hotkey('ctrl','f')
        time.sleep(2)
        pyautogui.write('de nova')
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('enter')
        time.sleep(15)
        #pyautogui.hotkey('ctrl','w')
        time.sleep(2)
        pyautogui.click(278,603)
        pyautogui.hotkey('tab')
        pyautogui.hotkey('enter')
        time.sleep(3)
        print('Terminou')
    
    
    def get_download(self):
    
        archive_name = os.listdir(self._save)[0]
        shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}4- CND FEDERAL.pdf")
        shutil.rmtree(self._save)
        time.sleep(2)
            
        for arquivo in os.listdir(self._pasta):
            if arquivo.find('4- CND FEDERAL.pdf') > -1:
                print('Download concluido para o cpf {}'.format(self._cnpj))        
                return 
        print('arquivo não foi gerado')
        raise TypeError('Erro não gero arquivo')