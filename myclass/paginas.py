from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from myclass.captcha import Captcha
from myclass.gb import Cut
from decouple import config
from db.class_mongo import Mongo
import time, random, os,json,urllib.request

class Paginas:
    def __init__(self,dados):
        self.login = False
        self.path_download = config('PATH_FILES')+dados.get('cpf')
        self.dados = dados
        self.tentativas = 0
        self.Erro = 0

        if dados.get('cpf') != "000.000.000-00":
            opt = webdriver.ChromeOptions()

            settings = {
                        "recentDestinations": [{
                            "id": "Save as PDF",
                            "origin": "local",
                            "account": "",
                        }],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2
                        }

            if config('HEADLESS') == True:
                opt.add_argument("--headless")

            opt.add_argument("--window-size=2560,1440")
            opt.add_argument("start-maximized")
            opt.add_argument("--disable-popup-blocking")
            opt.add_argument("ignore-certificate-errors")
            opt.add_argument('--kiosk-printing')

            opt.add_experimental_option( "prefs", {
                                                    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                                                    'savefile.default_directory': f'{self.path_download}',
                                                    'profile.default_content_settings.popups': 0,
                                                    'download.prompt_for_download' : False,
                                                    'download.default_directory': f'{self.path_download}',
                                                    'profile.default_content_setting_values.automatic_downloads':1
                                                })

            self.driver = webdriver.Chrome('/opt/drivers/chromedriver' , options=opt)
            self.driver.implicitly_wait(10)
            #driver.set_page_load_timeout(20)
            print("\033[32m"+"Pronto!, Chrome já esta inicializado."+"\033[0;0m")
        else:
            print("Não consigo criar a pasta.")

    def _login_esaj(self):
        self.driver.get(config('ESAJ_PAGE_LOGIN')) 
        self._existenciaPage("usernameForm") 
        self.driver.find_element(By.ID,"usernameForm").send_keys(f"{config('ESAJ_USER')}")
        self.driver.find_element(By.ID,"passwordForm").send_keys(f"{config('ESAJ_PASS')}")

        self.driver.find_element(By.ID,"pbEntrar").click()
        #ENQUANTO NÂO ACHAR O BOTAO SAIR, ELE VAI FICAR ESPERANDO PQ NÂO CONCLUIU O LOGIN
        while len(self.driver.find_elements(By.CLASS_NAME,"esajLogout")) < 1:
            time.sleep(1)

        self.login = True    

    def _existenciaPage(self,id):
        while len(self.driver.find_elements(By.ID, id)) < 1:
            print(f"não encontramos {id} na pagina")
            if int(self.tentativas) >= int(config('TENTATIVAS')):
                self.tentativas = 0
                break
            else:
                self.tentativas += 1
                time.sleep(0.5)

    def _select(self,id,value):
        while True:
                try:
                    select = Select(self.driver.find_element(By.ID, f"{id}"))
                    select.select_by_value(f'{value}')
                    self.tentativas = 0
                    break
                except:
                    if self.tentativas >= config('TENTATIVAS'):
                        break
                    else:
                        self.tentativas += 1
                        time.sleep(2)
                        pass
    
    def _update_extract(self,fild,_id):
        mongo = Mongo(config('MONGO_DB'))
        mongo._getcoll(config('MONGO_COLL'))
        mongo._update_one({'$set' :{f'extracted.{fild}': True}}, {'_id': _id})

    def _check_exists(self,parm):
        check_exists = False
        if 'extracted' in self.dados:
            if f'{parm}' in self.dados['extracted']:
                if self.dados['extracted'][f'{parm}'] == True:
                    check_exists = True

        return check_exists  

    def _CND_Estadual (self):  
        
        if not self._check_exists('_CND_ESTADUAL'):   
            try: 
                self.driver.get(config('PAGE_URL'))
                #VERIFICAR SE A PAGINA JA ESTA CARREGADA
                self._existenciaPage("MainContent_txtDocumento")
                self.driver.find_element(By.ID,"MainContent_txtDocumento").send_keys(f"{self.dados.get('cpf')}")
                c = Captcha(config('DATA_SITE_KEY'),config('PAGE_URL'))
                #print(f"Meu saldo atual é : {c._saldo()}.")
                wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
                self.driver.execute_script(wirte_tokon_js)
                time.sleep(1)
                self.driver.find_element(By.ID,"MainContent_btnPesquisar").click()
                time.sleep(0.5)
                #VOU VERIFICAR SE EXISTE O BOTÂO DE IMPRIMIR NA TELA, SE SIM CLICK NELE
                self._existenciaPage("MainContent_btnImpressao")   
                self.driver.find_element(By.ID,"MainContent_btnImpressao").click()

                del c
                time.sleep(4)
                self._update_extract('_CND_ESTADUAL', self.dados.get('_id')) 
            except:
                print("ERRO _CND_ESTADUAL")
                self.Erro = 1  

               

    def _CND_Municipal(self):
        if not self._check_exists('_CND_MUNICIPAL'): 
            try:
                self.driver.get(config('PAGE_URL_MUN'))
                self._select('ctl00_ConteudoPrincipal_ddlTipoCertidao','1')
                self._select('ctl00_ConteudoPrincipal_ddlTipoDocumento','CPF')
                time.sleep(0.8)
                self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_txtCPF").send_keys(f"{self.dados.get('cpf')}")

                namefile = random.randrange(99999)
                self.driver.save_screenshot("page_"+str(namefile)+".png")
                a = Cut()
                #CROP ARQUIVO DE PRINT TELA, NOME DO ARQUIVO QUANDO CORTADO
                image_cap = a.crop("page_"+str(namefile)+".png","crop_"+str(namefile)+".png")

                c = Captcha(image_cap,"")
                
                self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_txtValorCaptcha").send_keys(f"{c._resolve_img()}")
                time.sleep(0.5)
                self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_btnEmitir").click()
                #APAGAR OS ARQUIVOS GERADOS
                os.remove("page_"+str(namefile)+".png")
                os.remove("crop_"+str(namefile)+".png")

                del c               
                time.sleep(4)
                self._update_extract('_CND_MUNICIPAL', self.dados.get('_id')) 
            except:
                print("ERRO _CND_MUNICIPAL")
                self.Erro = 1   
             

    def _CND_Contribuinte(self):
        if not self._check_exists('_CND_CONTRIBUINTE'): 
            try:
                self.driver.get(config('PAGE_URL_CONTRIBUINTE'))
                self._existenciaPage("emitirCrda:crdaInputCpf")
                self.driver.find_element(By.ID,"emitirCrda:crdaInputCpf").send_keys(self.dados.get('cpf'))
                c = Captcha(config('DATA_SITE_KEY_CONTRIBUINTE'),config('PAGE_URL_CONTRIBUINTE'))
                #print(f"Meu saldo atual é : {c._saldo()}.")
                wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
                self.driver.execute_script(wirte_tokon_js)
                time.sleep(3)
                self.driver.find_element(By.XPATH,"//*[@id='emitirCrda:j_id136_body']/div[2]/input[2]").click()
                del c
                time.sleep(4)  
                self._update_extract('_CND_CONTRIBUINTE', self.dados.get('_id')) 
            except:
                print("ERRO _CND_CONTRIBUINTE")
                self.Erro = 1    
                        

    def _esaj_certidao(self,valor,print=False):
        if not self._check_exists(f'_ESAJ_CERTIDAO_{valor}'): 
            try:
                if self.login == False:
                    self._login_esaj()
                    self._esaj_certidao(valor)
                else:    
                    genero = self.dados.get("genero")
                    self.driver.get(config('PAGE_URL_CRIMINAL_1'))
                    self._select("cdModelo",valor)
                    time.sleep(1)
                    self.driver.find_element(By.ID,"nmCadastroF").send_keys(self.dados.get("nome"))
                    self.driver.find_element(By.ID,"identity.nuCpfFormatado").send_keys(self.dados.get("cpf"))
                    self.driver.find_element(By.ID,"identity.nuRgFormatado").send_keys(self.dados.get("rg"))

                    self.driver.find_element(By.ID,f"flGenero{genero}").click()

                    if valor == "6":
                        self.driver.find_element(By.ID,"nmMaeCadastro").send_keys(self.dados.get("mae"))
                        self.driver.find_element(By.ID,"dataNascimento").send_keys(self.dados.get("nascimento"))

                    self.driver.find_element(By.ID,"identity.solicitante.deEmail").send_keys(config('EMAILESAJ'))
                    self.driver.find_element(By.ID,"confirmacaoInformacoes").click()
                    time.sleep(1)
                    self.driver.find_element(By.ID,"pbEnviar").click()

                    while True:               
                        try:
                            self.driver.find_element(By.ID,"btnSim").click()
                            self.tentativas = 0
                            break
                        except:
                            if int(self.tentativas) < int(config('TENTATIVAS')) :
                                self.tentativas += 1
                                time.sleep(1)
                                pass   
                            else:
                                self.tentativas = 0
                                print("Esgotou as tentativas")
                                break 

                    print("Rodou esaj.")
                    time.sleep(4)

                    if print:
                        try:
                            self.driver.execute_script('window.print();')
                        except:
                            print("Não conseguiu printar a tela")

                    self._update_extract(f'_ESAJ_CERTIDAO_{valor}', self.dados.get('_id'))
            except:
                print(f"ERRO _ESAJ_CERTIDAO_{valor}")
                self.Erro = 1

    def _trtsp(self):
        if not self._check_exists('_TRTSP'): 
            try:
                namefile = random.randrange(99999)
                self.driver.get(config('PAGE_URL_TRTSP'))
                self._existenciaPage("numeroDocumentoPesquisado")
                self.driver.find_element(By.ID,"numeroDocumentoPesquisado").send_keys(self.dados.get('cpf'))
                self.driver.find_element(By.ID,"nomePesquisado").send_keys(self.dados.get('nome'))
                urlimage = self.driver.find_element(By.XPATH,"//*[@id='captcha-element']/table/tbody/tr[1]/td[1]/img").get_attribute("src")
                urllib.request.urlretrieve(urlimage, "page_"+str(namefile)+".png")
                
                a = Cut()
                image_cap = a._converte_image_to_base64("page_"+str(namefile)+".png")
                c = Captcha(image_cap,"")
                self.driver.find_element(By.ID,"captcha-input").send_keys(c._resolve_img())
                self.driver.find_element(By.ID,"submit").click()

                os.remove("page_"+str(namefile)+".png")

                while True:
                    try:
                        if self.driver.page_source.find("Visualizar Certidão"):
                            self.driver.find_element(By.XPATH,"//*[@id='main-content']/div/fieldset/button").click()
                            self.tentativas = 0
                            break
                        else:
                            pass         
                    except:

                        if int(self.tentativas) < int(config('TENTATIVAS')):
                            print("Não apareceu o imprimir ainda")
                            self.tentativas += 1
                            time.sleep(1)
                            pass
                        else:
                            print("Não conseguiu resolver TRT SP")
                            self.tentativas = 0
                            break

                time.sleep(4) 
                self._update_extract('_TRTSP', self.dados.get('_id'))
            except:
                print("ERRO _TRTSP")
                self.Erro = 1   
                  
    def _tst_trabalhista(self):
        if not self._check_exists('_TST_TRABALHISTA'): 
            try:
                self.driver.get(config('PAGE_URL_TST'))
                self._existenciaPage("corpo")
                self.driver.find_element(By.XPATH,"//*[@id='corpo']/div/div[2]/input[1]").click()
                while True:
                    try:
                        image_cap = self.driver.find_element(By.ID,"idImgBase64").get_attribute("src")
                        print(image_cap.replace("data:image/png;base64, ",""))
                        break
                    except:
                        time.sleep(0.5)
                        pass  
                c = Captcha(image_cap,"")
                self.driver.find_element(By.ID,"gerarCertidaoForm:cpfCnpj").send_keys(self.dados.get('cpf'))
                self.driver.find_element(By.ID,"idCaptcha").send_keys(c._resolve_img())
                self.driver.find_element(By.ID,"gerarCertidaoForm:btnEmitirCertidao").click()
                del c
                time.sleep(4)
                self._update_extract('_TST_TRABALHISTA', self.dados.get('_id'))
            except:
                print("ERRO _TST_TRABALHISTA")    
                self.Erro = 1 
            

    def _trt15(self):
        if not self._check_exists('_TRT15'): 
            try:
                namefile = random.randrange(999999999)
                self.driver.get(config('PAGE_URL_TRT15'))
                self._existenciaPage("certidaoActionForm:j_id23:doctoPesquisa")
                self.driver.find_element(By.ID,"certidaoActionForm:j_id23:doctoPesquisa").send_keys(self.dados.get('cpf'))

                self.driver.save_screenshot("page_"+str(namefile)+".png")
                a = Cut()
                #CROP ARQUIVO DE PRINT TELA, NOME DO ARQUIVO QUANDO CORTADO
                image_cap = a.crop("page_"+str(namefile)+".png","crop_"+str(namefile)+".png",215,250,62,132)
                c = Captcha(image_cap,"")
                self.driver.find_element(By.ID,"certidaoActionForm:j_id51:verifyCaptcha").send_keys(c._resolve_img())
                self.driver.find_element(By.ID,"certidaoActionForm:certidaoActionEmitir").click()

                self._existenciaPage("certidaoActionForm:certidaoActionImprimir")
                self.driver.find_element(By.ID,"certidaoActionForm:certidaoActionImprimir").click()

                del c
                del a
                os.remove("page_"+str(namefile)+".png")
                os.remove("crop_"+str(namefile)+".png")

                time.sleep(4)
                self._update_extract('_TRT15', self.dados.get('_id'))
            except:
                print("ERRO _TRT15")    
                self.Erro = 1 

    def _esaj_busca_nome_cpf(self,parm):
        if not self._check_exists(f'_ESAJ_BUSCA_{parm}'): 
            try:
                if self.login == False:
                    self._login_esaj()
                    self._esaj_busca_nome_cpf(parm)
                else:
                    self.driver.get(config('PAGE_URL_ESAJ_B_NOME_CPF'))
                    self._existenciaPage("botaoConsultarProcessos")  
                    
                    if parm == "NOME":
                        ValueSelect = "NMPARTE"
                        ValueInput = self.dados.get('nome')
                    else:
                        ValueSelect = "DOCPARTE"  
                        ValueInput = self.dados.get('cpf')

                    self._select("cbPesquisa",ValueSelect)
                    self.driver.find_element(By.ID, f"campo_{ValueSelect}").send_keys(ValueInput)
                    self.driver.find_element(By.ID,"botaoConsultarProcessos").click()
                    time.sleep(4)
                    self.driver.execute_script('window.print();')
                    time.sleep(1)
                    #self.driver.save_screenshot(f"{self.path_download}/print_tela_{ValueSelect}.png")
                    self._update_extract(f'_ESAJ_BUSCA_{parm}', self.dados.get('_id'))
            except:
                print(f"ERRO _ESAJ_BUSCA_{parm}")  
                self.Erro = 1       

    def _protestos(self):
        if not self._check_exists('_PROTESTOS'): 
            try:
                self.driver.get(config('PAGE_URL_PROTESTO'))
                self._existenciaPage("AbrangenciaNacional")
                self.driver.execute_script("document.getElementById('cf-root').style.display = 'none'")
                self.driver.find_element(By.ID,"AbrangenciaNacional").click()
                self._select("TipoDocumento","1")
                self.driver.find_element(By.ID,"Documento").send_keys(self.dados.get('cpf'))
                self.driver.execute_script("ValidarConsulta(this)")
                time.sleep(4)

                if self.driver.page_source.find("o recaptcha do Google identificou um acesso inesperado") > -1:
                    print("O robô esta sofrendo um bloqueio de ip")
                else:    
                    self.driver.execute_script("document.getElementById('cf-root').style.display = 'none'")
                #self.driver.save_screenshot(f"{self.path_download}/print_tela_protesto.png")
                time.sleep(4)
                self.driver.execute_script('window.print();')
                time.sleep(1)
                self._update_extract('_PROTESTOS', self.dados.get('_id')) 
            except:
                print("ERRO _PROTESTO")  
                self.Erro = 1      
        
