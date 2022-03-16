from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from myclass.captcha import Captcha
from myclass.gb import Cut
from decouple import config
import time, random, os,json,urllib.request

class Paginas:
    def __init__(self,cpf='000'):
        self.login = False
        self.path_download = config('PATH_FILES')+cpf
        if cpf != "000":
            opt = webdriver.ChromeOptions()

            if config('HEADLESS') == True:
                opt.add_argument("--headless")

            opt.add_argument("--window-size=2560,1440")
            opt.add_argument("start-maximized")
            opt.add_argument("--disable-xss-auditor")
            opt.add_argument("--disable-web-security")
            opt.add_argument("--allow-running-insecure-content")
            opt.add_argument("--no-sandbox")
            opt.add_argument("--disable-setuid-sandbox")
            opt.add_argument("--disable-webgl")
            opt.add_argument("--disable-popup-blocking")
            opt.add_argument("ignore-certificate-errors")

            opt.add_experimental_option( "prefs", {
                                                    'profile.default_content_settings.popups': 0,
                                                    'download.prompt_for_download' : False,
                                                    'download.default_directory': f'{self.path_download}',
                                                    'profile.default_content_setting_values.automatic_downloads':1
                                                })

            self.driver = webdriver.Chrome('/opt/drivers/chromedriver' , options=opt)
            #driver.implicitly_wait(10)
            #driver.set_page_load_timeout(20)
            print("Pronto!, Chrome já esta inicializado.")
            r = Captcha("","")
            print(f"Meu saldo no 2Captch : {r._saldo()}")
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
            time.sleep(0.5)

    def _select(self,id,value):
        while True:
                try:
                    select = Select(self.driver.find_element(By.ID, f"{id}"))
                    select.select_by_value(f'{value}')
                    break
                except:
                    time.sleep(2)
                    pass
    
    def _CND_Estadual (self,cpf='000'):
        if cpf != "000":
            
            self.driver.get(config('PAGE_URL'))
            #VERIFICAR SE A PAGINA JA ESTA CARREGADA
            self._existenciaPage("MainContent_txtDocumento")
            self.driver.find_element(By.ID,"MainContent_txtDocumento").send_keys(f"{cpf}")
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
        else:
            print("Ausencia de parametros para consulta.")

    def _CND_Municipal(self,cpf='000'):
        if cpf != "000":
            self.driver.get(config('PAGE_URL_MUN'))
            self._select('ctl00_ConteudoPrincipal_ddlTipoCertidao','1')
            self._select('ctl00_ConteudoPrincipal_ddlTipoDocumento','CPF')
            time.sleep(0.8)
            self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_txtCPF").send_keys(f"{cpf}")

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
        else:
            print("Ausencia de parametros para consulta.")

    def _CND_Contribuinte(self,cpf='000'):
        if cpf != "000":
            self.driver.get(config('PAGE_URL_CONTRIBUINTE'))
            self._existenciaPage("emitirCrda:crdaInputCpf")
            self.driver.find_element(By.ID,"emitirCrda:crdaInputCpf").send_keys(f"{cpf}")
            c = Captcha(config('DATA_SITE_KEY_CONTRIBUINTE'),config('PAGE_URL_CONTRIBUINTE'))
            #print(f"Meu saldo atual é : {c._saldo()}.")
            wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
            self.driver.execute_script(wirte_tokon_js)
            time.sleep(3)
            self.driver.find_element(By.XPATH,"//*[@id='emitirCrda:j_id136_body']/div[2]/input[2]").click()

            del c

            time.sleep(4)
        else:
            print("Ausencia de parametros para consulta.")               

    def _esaj_certidao(self,dados):
        
        if self.login == False:
            self._login_esaj()
            self._esaj_certidao(dados)
        else:    
            genero = dados.get("genero")
            self.driver.get(config('PAGE_URL_CRIMINAL_1'))
            self._select("cdModelo","6")
            time.sleep(1)
            self.driver.find_element(By.ID,"nmCadastroF").send_keys(dados.get("nome"))
            self.driver.find_element(By.ID,"identity.nuCpfFormatado").send_keys(dados.get("cpf"))
            self.driver.find_element(By.ID,"identity.nuRgFormatado").send_keys(dados.get("rg"))

            self.driver.find_element(By.ID,f"flGenero{genero}").click()
            self.driver.find_element(By.ID,"nmMaeCadastro").send_keys(dados.get("mae"))
            self.driver.find_element(By.ID,"dataNascimento").send_keys(dados.get("nascimento"))
            self.driver.find_element(By.ID,"confirmacaoInformacoes").click()
            self.driver.find_element(By.ID,"pbEnviar").click()
            tentativa = 0
            while True:               
                try:
                    if self.driver.page_source.find("Já foi cadastrado um pedido de certidão para este"):
                        self.driver.find_element(By.ID,"btnSim").click()
                        break
                except:
                    if tentativa < 2 :
                        tentativa += 1
                        time.sleep(1)
                        pass   
                    else:
                        break 

            self._existenciaPage("pbImprimir")

            self.driver.save_screenshot(f"{self.path_download}/print_tela_esaj.png")

    def _trtsp(self,dados):
        namefile = random.randrange(99999)
        self.driver.get(config('PAGE_URL_TRTSP'))
        self._existenciaPage("numeroDocumentoPesquisado")
        self.driver.find_element(By.ID,"numeroDocumentoPesquisado").send_keys(dados.get('cpf'))
        self.driver.find_element(By.ID,"nomePesquisado").send_keys(dados.get('nome'))
        urlimage = self.driver.find_element(By.XPATH,"//*[@id='captcha-element']/table/tbody/tr[1]/td[1]/img").get_attribute("src")
        urllib.request.urlretrieve(urlimage, "page_"+str(namefile)+".png")
        
        a = Cut()
        image_cap = a._converte_image_to_base64("page_"+str(namefile)+".png")
        c = Captcha(image_cap,"")
        self.driver.find_element(By.ID,"captcha-input").send_keys(c._resolve_img())
        self.driver.find_element(By.ID,"submit").click()

        os.remove("page_"+str(namefile)+".png")

        tentativas = 0

        while True:
            try:
                if self.driver.page_source.find("Visualizar Certidão"):
                    self.driver.find_element(By.XPATH,"//*[@id='main-content']/div/fieldset/button").click()
                    break
                else:
                    pass         
            except:

                if tentativas < 2:
                    print("Não apareceu o imprimir ainda")
                    tentativas += 1
                    time.sleep(1)
                    pass
                else:
                    print("Não conseguiu resolver TRT SP")
                    break

        time.sleep(4)
        print("Final...")        
    
    def _tst_trabalhista(self, cpf):
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
        print(f"Meu saldo atual é : {c._saldo()}.")

        self.driver.find_element(By.ID,"gerarCertidaoForm:cpfCnpj").send_keys(cpf)
        self.driver.find_element(By.ID,"idCaptcha").send_keys(c._resolve_img())
        self.driver.find_element(By.ID,"gerarCertidaoForm:btnEmitirCertidao").click()
        del c
        time.sleep(4)

    def _trt15(self,cpf="000"):
        namefile = random.randrange(999999999)
        self.driver.get(config('PAGE_URL_TRT15'))
        self._existenciaPage("certidaoActionForm:j_id23:doctoPesquisa")
        self.driver.find_element(By.ID,"certidaoActionForm:j_id23:doctoPesquisa").send_keys(cpf)

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

    def _trf3_jus(self,dados):
        self.driver.get(config('PAGE_URL_TRF3_JUS'))
        self._existenciaPage("Nome")
        self.driver.find_element(By.ID,"abrangenciaSJSP").click()
        self.driver.find_element(By.ID,"Nome").send_keys(dados.get('nome'))
        #self.driver.find_element(By.ID,"CpfCnpj").send_keys(dados.get('cpf'))
        self.driver.execute_script(f"document.getElementById('CpfCnpj').value = '{dados.get('cpf')}'")

        #RECAPTCHA
        #c = Captcha(config('DATA_SITE_KEY_TRF3_JUS'),config('PAGE_URL_TRF3_JUS'))
        #c._resolve()

        #wirte_tokon_js = f'document.getElementById("g-recaptcha-response-100000").innerHTML="{c._resolve()}";'
        #self.driver.execute_script(wirte_tokon_js)

        self.driver.find_element(By.ID,"BtGeraCerticao").click()

        time.sleep(1000)

    def _esaj_busca_nome_cpf(self,dados,parm):
        if self.login == False:
            self._login_esaj()
            self._esaj_busca_nome_cpf(dados,parm)
        else:
            self.driver.get(config('PAGE_URL_ESAJ_B_NOME_CPF'))
            self._existenciaPage("botaoConsultarProcessos")  
            
            if parm == "nome":
                ValueSelect = "NMPARTE"
                ValueInput = dados.get('nome')
            else:
                ValueSelect = "DOCPARTE"  
                ValueInput = dados.get('cpf')

            self._select("cbPesquisa",ValueSelect)
            self.driver.find_element(By.ID, f"campo_{ValueSelect}").send_keys(ValueInput)
            self.driver.find_element(By.ID,"botaoConsultarProcessos").click()
            time.sleep(4)
            self.driver.save_screenshot(f"{self.path_download}/print_tela_{ValueSelect}.png")

    def _protestos(self,dados):
        self.driver.get(config('PAGE_URL_PROTESTO'))
        self._existenciaPage("AbrangenciaNacional")
        self.driver.execute_script("document.getElementById('cf-root').style.display = 'none'")
        self.driver.find_element(By.ID,"AbrangenciaNacional").click()
        self._select("TipoDocumento","1")
        self.driver.find_element(By.ID,"Documento").send_keys(dados.get('cpf'))
        self.driver.execute_script("ValidarConsulta(this)")
        time.sleep(4)
        self.driver.execute_script("document.getElementById('cf-root').style.display = 'none'")
        self.driver.save_screenshot(f"{self.path_download}/print_tela_protesto.png")
        time.sleep(4)
        
