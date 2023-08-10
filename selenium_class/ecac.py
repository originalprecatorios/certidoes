from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import os, time, shutil
from utils.firefox_download import TEXTO
from crypto import db
import undetected_chromedriver as uc
from decouple import config

class Ecac:

    def __init__(self,pData,pLink,pMongo,pCaptcha):
        print('Robo ECAC')
        self._data = pData
        self._link = pLink
        self._bdMongo = pMongo
        self._captcha = pCaptcha
        self._save = '/opt/certidao/download/ecac{}'.format(self._data['cpf'])
        self._pasta = self._data['path']
        self._capt = '/tmp/captcha/'
        
        for caminhos in [self._pasta,self._capt]:
            self.create_folder(caminhos)
        try:
            if os.path.isdir(f'{self._save}') is False:
                os.makedirs(f'{self._save}')
            else:
                shutil.rmtree(self._save)
                os.makedirs(f'{self._save}')
        except:
            pass
        
    def create_folder(self,pPath):
        if os.path.isdir(f'{pPath}'):
            print("O diretório existe!")
        else:
            os.makedirs(f'{pPath}')
    
    def firefox(self,link):
        #fp = webdriver.FirefoxProfile()
        options = Options()
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", self._save)
        options.set_preference(TEXTO[0], TEXTO[1])
        options.set_preference("pdfjs.disabled", True)
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)
        self._driver.get(link)
        time.sleep(2)
    
    def chrome(self,link):
        options = uc.ChromeOptions()
        options.add_argument('--no-first-run')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--window-size=2560,1440")
        options.add_argument('--no-sandbox')
        options.add_experimental_option('prefs', {
        "download.default_directory": f"{self._save}", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        self._driver = uc.Chrome(options=options,version_main=int(config('VERSION')))
        try:
            self._driver.set_page_load_timeout(60)
        except:
            pass
        #MUDAR A PARSTA DE DOWNLOAD
        params = {
            "behavior": "allow",
            "downloadPath": self._save
        }

        self._driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
        time.sleep(1)
        print('Navegando no site')
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                     'Chrome/85.0.4183.102 Safari/537.36'})
        self._driver.get(link)
    
    def create_password(self):
        try:
            lista_data = []
            self.firefox(self._link)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtCPF"))).send_keys(self._data['cpf'])
            data_obj = datetime.strptime(self._data['nascimento'], '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
            while True:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtCPF"))).send_keys('0'+data_formatada)
                WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "img_captcha_serpro_gov_br")))
                time.sleep(2)
                with open(f'{self._capt}captcha.png', 'wb') as file:
                    l = self._driver.find_element(By.ID,'img_captcha_serpro_gov_br')
                    file.write(l.screenshot_as_png)
                time.sleep(2)
                response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
                if response is None:
                    response = self._captcha.resolve_normal(os.path.join(self._capt,'captcha.png'))
                #response = ''
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtCaptcha"))).send_keys(response)
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "btnAvancar"))).click()
                time.sleep(5)
                try:
                    alerta = self._driver.switch_to.alert
                    alerta.accept()
                    break
                except:
                    print('Não existe chave anterior gerada')
                    pass
                try:
                    validation = WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "ValidationSummary1"))).text
                    if validation == 'Caracteres da imagem não conferem.':
                        print('Caracteres da imagem não conferem.')
                    else:
                        break
                except:
                    break  
            
            try:
                caixa_mensagem = WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "caixaMensagem"))).text
                if caixa_mensagem.find('Você não apresentou declaração de imposto de renda (DIRPF) como titular em nenhum dos dois últimos exercícios.') >=0:
                    return 'Sem declaração'
            except:
                print('Existe declarações de imposto de renda')
                pass
            try:
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "line"))).text
                irpf = self._driver.find_elements(By.CLASS_NAME,'line')[3].text
                if len(self._data['numero_recibo_irpf']) <=1:
                    try:
                        irpf_separado = irpf.split(':\n')[1].split(' ')
                        if len(irpf_separado) > 1:
                            for ir in range(1,len(irpf_separado)):
                                lista_data.append(irpf_separado[ir])
                            self._driver.close()
                            return False, lista_data
                    except:
                        pass            
                creat_pass = self._data['cpf'].replace('.','').replace('-','')+self._data['nome'].split()[0].capitalize()
                cont = 1
                for recibo in self._data['numero_recibo_irpf']:
                    WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtReciboAno{}".format(cont)))).send_keys(self._data['numero_recibo_irpf'][recibo].replace('.','').replace('-',''))
                    cont += 1
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtSenha"))).send_keys(creat_pass)
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "txtConfirmaSenha"))).send_keys(creat_pass)
                WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "btnGerarCodigo"))).click()
                return_pass = WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "frmPrincipal"))).text
                cripto_creat_pass = db.encrypt(creat_pass)
                cpf = db.encrypt(self._data['cpf'])
                arr = {
                        'code': return_pass.split('\n')[1],
                        'password': cripto_creat_pass,
                        'validity': return_pass.split('\n')[3].split(':')[1],
                        'cpf': cpf,
                        'name': self._data['nome']
                }
                self._bdMongo._getcoll('password_ecac')
                bd = {'name':self._data['nome'],'cpf':cpf}
                self._bdMongo._upsert({'$set':arr},bd)
                self._driver.close()
                return True,arr
            except:
                #self._driver.close()
                return False,''


        except Exception as e:
            self._driver.close()
            print(e)
            return
    
    def login(self,arr):
        try:
            self.chrome('https://cav.receita.fazenda.gov.br/autenticacao/Login')
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "NI"))).send_keys(db.decrypt(arr['cpf']).replace('.','').replace('-',''))
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "CodigoAcesso"))).send_keys(arr['code'])
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "Senha"))).send_keys(db.decrypt(arr['password']))
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "submit"))).click()
            time.sleep(5)
            try:
                logado = WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "bem-vindo"))).text
                if logado.find('Seja bem-vindo ao Portal e-CAC da Receita Federal') < 0:
                    return False
            except:
                return False
            self._driver.execute_script("window.open('https://cav.receita.fazenda.gov.br/ecac/Aplicacao.aspx?id=2&origem=maisacessados', '_blank')")
            self._driver.switch_to.window(self._driver.window_handles[1])
            time.sleep(2)
            iframe = self._driver.find_element(By.ID,"frmApp")
            self._driver.switch_to.frame(iframe)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "menuPrincipal_divLinks3"))).click()
            time.sleep(2)
            iframe = self._driver.find_element(By.ID,"palco")
            self._driver.switch_to.frame(iframe)
            WebDriverWait(self._driver, 3).until(EC.presence_of_element_located((By.ID, "validar"))).click()
            time.sleep(5)
            archive_name = os.listdir(self._save)[0]
            shutil.move(f"{self._save}/{archive_name}", f"{self._pasta}FEDERAL ECAC.pdf")
            shutil.rmtree(self._save)
            time.sleep(2)
            self._driver.close()
            time.sleep(2)
            time.sleep(2)
            self._driver.switch_to.window(self._driver.window_handles[0])
            self._driver.close()
            for arquivo in os.listdir(self._pasta):
                if arquivo.find('FEDERAL ECAC.pdf') > -1:
                    print('Download do arquivo gerado para o cliente {}'.format(self._data['nome']))
                    return True
            print('arquivo não foi gerado')
            self._driver.close()

            


        except Exception as e:
            self._driver.close()
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.ID, "submit")))
            self._driver.find_element(By.ID,'submit').click()
        

    ########## looping até o download concluir 
    def _download(self):
        
        while True:
            cont = 0
            for arquivo in os.listdir(self._save):
                if arquivo.find('crdownload') > -1 and cont <= 6:
                    print('Aguardando término do download')
                    time.sleep(5)
                    cont += 1
                else:
                    return
            return