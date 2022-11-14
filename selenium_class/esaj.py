from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pathlib import Path
from decouple import config
import time, os

class Esaj:

    def __init__(self,pData,pLink,pMongo, pError,pCaptcha):
        print('Robo Esaj')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._error = pError
        self._captcha = pCaptcha
        self._error._getcoll('error')
    
        fp = webdriver.FirefoxProfile()
        fp.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("pdfjs.disabled", True)
        options = Options()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(firefox_profile=fp)
        self._driver.get(self._link)
        time.sleep(2)
        
        
    
    def login(self):
        try:    
            self._driver.get(config('ESAJ_PAGE_LOGIN')) 
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "usernameForm")))
            self._driver.find_element(By.ID,"usernameForm").send_keys(f"{config('ESAJ_USER')}")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "passwordForm")))
            self._driver.find_element(By.ID,"passwordForm").send_keys(f"{config('ESAJ_PASS')}")
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "pbEntrar")))
            self._driver.find_element(By.ID,"pbEntrar").click()
            time.sleep(5)
        
        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            
            return
    
    def get_data(self,pSelect):
        try:    
            self._driver.get(config('PAGE_URL_CRIMINAL_1'))
            time.sleep(2)
            select = Select(self._driver.find_element(By.ID, 'cdModelo'))
            select.select_by_value(f'{pSelect}')
            time.sleep(2)

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "nmCadastroF")))
            self._driver.find_element(By.ID,"nmCadastroF").send_keys(self._data['nome'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "identity.nuCpfFormatado")))
            self._driver.find_element(By.ID,"identity.nuCpfFormatado").send_keys(self._data['cpf'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "identity.nuRgFormatado")))
            self._driver.find_element(By.ID,"identity.nuRgFormatado").send_keys(self._data['rg'])
            self._driver.find_element(By.ID,f"flGenero{self._data['sexo']}").click()

            if pSelect == "6":
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "nmMaeCadastro")))
                self._driver.find_element(By.ID,"nmMaeCadastro").send_keys(self._data['mae'])
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "dataNascimento")))
                data = self._data['nascimento'].split('-')[2]+self._data['nascimento'].split('-')[1]+self._data['nascimento'].split('-')[0]

                self._driver.find_element(By.ID,"dataNascimento").send_keys(data)

            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "identity.solicitante.deEmail")))
            self._driver.find_element(By.ID,"identity.solicitante.deEmail").send_keys(self._data['email'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "confirmacaoInformacoes")))
            self._driver.find_element(By.ID,"confirmacaoInformacoes").click()
            time.sleep(1)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "pbEnviar")))
            self._driver.find_element(By.ID,"pbEnviar").click()

            try:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "btnSim")))
                self._driver.find_element(By.ID,'btnSim').click()
            except:
                pass

            time.sleep(3)
            print('Download enviado por email')
            self._driver.close()
        
        except Exception as e:
            self._driver.close()
            err = {'data':str(datetime.today()).split(' ')[0].replace('-',''),
                    'dado_utilizado': self._data['nome'],
                    'sistema': 'municipal',
                    'funcao' : 'erro na função login',
            }
            self._error.addData(err)
            
            return