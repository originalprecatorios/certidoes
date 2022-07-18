from myclass.captcha import Captcha
from decouple import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver.v2 as uc
#from db.class_mongo import Mongo
import time, os

class Nodistill:

    def __init__(self,dados):
        self.path_download = config('PATH_FILES')+dados.get('cpf')
        self.dados = dados
        self.tentativas = 0
        self.Erro = 0 
        self.OpenBrowser = 0

    def _navegador(self):
        if self.OpenBrowser == 0:
            options = uc.ChromeOptions()
            options.add_argument('--no-first-run')
            options.add_argument("--window-size=2560,1440")
            options.add_argument('--no-sandbox')
            self.driver = uc.Chrome(options=options, version_main=89)
            #MUDAR A PARSTA DE DOWNLOAD
            params = {
                "behavior": "allow",
                "downloadPath": self.path_download
            }

            self.driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

            if not os.path.isdir(f"{config('PATH_FILES')}{self.dados.get('cpf')}"):
                os.mkdir(f"{config('PATH_FILES')}{self.dados.get('cpf')}")

            self.OpenBrowser = 1
        else:
            pass

    def _existenciaItem(self,id):
        while len(self.driver.find_elements(By.ID, id)) < 1:
            print(f"não encontramos {id} na pagina")
            if int(self.tentativas) >= int(config('TENTATIVAS')):
                self.tentativas = 0
                break
            else:
                self.tentativas += 1
                time.sleep(0.5) 
    def _wait(self):
        self.wait = WebDriverWait(self.driver, 120)

    def _existenciaPage(self,id):    
        self.wait.until(EC.presence_of_element_located((By.ID, id)))            

    def _check_exists(self,parm):
        check_exists = False
        if 'extracted' in self.dados:
            if f'{parm}' in self.dados['extracted']:
                if self.dados['extracted'][f'{parm}'] == True:
                    check_exists = True

        return check_exists
         

    def _update_extract(self,fild,_id):
        mongo = Mongo(config('MONGO_DB'))
        mongo._getcoll(config('MONGO_COLL'))
        mongo._update_one({'$set' :{f'extracted.{fild}': True}}, {'_id': _id})

    def _pje_trf3(self):
        if 'extracted' not in self.dados:
            try:
                self.driver.get(config('PAGE_URL_PJE_TRF3'))
                self._existenciaPage("fPP:dpDec:documentoParte")
                self.driver.find_element(By.ID,"fPP:dpDec:documentoParte").send_keys(self.dados.get('cpf'))
                self.driver.find_element(By.ID,"fPP:searchProcessos").click()

                c = Captcha(config('DATA_SITE_KEY_HCAPTCHA_PJE'),config('PAGE_URL_PJE_TRF3'),'hcaptcha')
                resp = c._resolve()
                #PEGAR O data-hcaptcha-widget-id DO FRAME
                id = self.driver.find_element(By.XPATH,"//*[@id='fPP:j_id236']/div/iframe").get_attribute("data-hcaptcha-widget-id")
                self.driver.execute_script(f'document.getElementById("h-captcha-response-{id}").innerHTML="{resp}";')
                #CALLBACK
                self.driver.execute_script("A4J.AJAX.Submit('fPP',event,{'similarityGroupingId':'fPP:searchProcessos','parameters':{'fPP:searchProcessos':'fPP:searchProcessos'} } )")    
                time.sleep(4)
                self._update_extract('_PJE_TRF3', self.dados.get('_id')) 
            except:
                print("ERRO - _PJE_TRF3")
                self.Erro = 1     
                 

    def _CND_Federal(self):
        if not self._check_exists('_CND_FEDERAL'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_FEDERAL'))
                self._wait()
                self._existenciaPage("NI")
                self.driver.find_element(By.ID,"NI").send_keys(self.dados.get('cpf'))
                time.sleep(0.8)
                self.driver.find_element(By.ID,"validar").click()
                self._existenciaItem("FrmSelecao")

                try:
                    
                    url = self.driver.find_element(By.XPATH,"//*[@id='FrmSelecao']/a[1]").get_attribute("href")
                    self.driver.get(url)
                    self._existenciaPage("PeriodoInicio")
                    time.sleep(0.8)
                    self.driver.find_element(By.ID,"validar").click()
                    self._existenciaItem("resultado")
                    self.driver.find_element(By.XPATH,"//*[@id='resultado']/table/tbody/tr[1]/td[7]/a").click()
                except:
                    print("Não encontrado o link")

                time.sleep(4)
                self._update_extract('_CND_FEDERAL', self.dados.get('_id'))
            except Exception as e:
                print("Erro ocorrido ao rodar o _CND_FEDERAL" + str(e))
                self.Erro = 1           

    def _trf3_jus(self,tipo):
        if not self._check_exists(f'_TRF3_JUS_{tipo}'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_TRF3_JUS'))
                self._wait()
                self._existenciaPage("Nome")
                self.driver.find_element(By.ID, f"abrangencia{tipo}").click()
                self.driver.find_element(By.ID,"Nome").send_keys(self.dados.get('nome'))
                time.sleep(0.8)
                self.driver.execute_script(f"document.getElementById('CpfCnpj').value = '{self.dados.get('cpf')}'")
                time.sleep(0.8)
                self.driver.find_element(By.ID,"BtGeraCerticao").click()

                while True:
                    if self.driver.page_source.find("Gerar PDF") > -1:
                        self.driver.find_element(By.XPATH,"//*[@id='frm']/p/a").click()
                        self.tentativas = 0
                        break
                    else:
                        print("Não existe ainda")
                        if int(self.tentativas) >= int(config('TENTATIVAS')):
                            self.tentativas = 0
                            break
                        else:
                            self.tentativas += 1
                            time.sleep(2) 
                            pass
                        
                        
                time.sleep(4) 
                self._update_extract(f'_TRF3_JUS_{tipo}', self.dados.get('_id'))    
            except:
                print(f"Erro ocorrido ao rodar _trf3_jus_{tipo}")  
                self.Erro = 1      

