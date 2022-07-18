from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from myclass.captcha import Captcha
from myclass.gb import Cut
from decouple import config
#from db.class_mongo import Mongo
import time, random, os,json,urllib.request

class Paginas:
    def __init__(self,dados):
        self.login = False
        self.path_download = f"{config('PATH_FILES')}{dados.get('cpf')}"
        self.dados = dados
        self.tentativas = 0
        self.Erro = 0
        self.OpenBrowser = 0
        

    def _navegador(self):
        if self.OpenBrowser == 0:
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
            opt.add_argument('--no-sandbox')
            opt.add_argument('--disable-dev-shm-usage') 
            opt.add_argument('--kiosk-printing')
            opt.add_experimental_option( "prefs", {
                                                    'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                                                    'savefile.default_directory': f'{self.path_download}',
                                                    'profile.default_content_settings.popups': 0,
                                                    'download.prompt_for_download' : False,
                                                    'download.default_directory': f'{self.path_download}',
                                                    'profile.default_content_setting_values.automatic_downloads':1
                                                })
            capa = DesiredCapabilities.CHROME
            capa["pageLoadStrategy"] = "none"

            self.driver = webdriver.Chrome(desired_capabilities=capa,executable_path='/opt/drivers/chromedriver' , options=opt)
            print("\033[32m"+"Pronto!, Chrome já esta inicializado."+"\033[0;0m")
            self.OpenBrowser = 1
            self.wait = WebDriverWait(self.driver, 120)
        else:
            pass
	
    def _espera(self):
        time.sleep(5)
    def _existenciaPage(self,id):
        self.wait.until(EC.presence_of_element_located((By.ID, id)))

    def _existenciaItem(self,id):
        ind = False
        while len(self.driver.find_elements(By.ID, id)) < 1:
            print(f"não encontramos {id} na pagina")
            if int(self.tentativas) >= int(config('TENTATIVAS')):
                self.tentativas = 0
                ind = True
                break
            else:
                self.tentativas += 1
                time.sleep(0.5)

        return ind       

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

    def _login_esaj(self):
        if self.login == False:
            self._navegador()
            self.driver.get(config('ESAJ_PAGE_LOGIN')) 
            self._espera()
            self._existenciaPage("usernameForm") 
            self.driver.find_element(By.ID,"usernameForm").send_keys(f"{config('ESAJ_USER')}")
            self.driver.find_element(By.ID,"passwordForm").send_keys(f"{config('ESAJ_PASS')}")

            self.driver.find_element(By.ID,"pbEntrar").click()
            time.sleep(4)
            #ENQUANTO NÂO ACHAR O BOTAO SAIR, ELE VAI FICAR ESPERANDO PQ NÂO CONCLUIU O LOGIN
            while len(self.driver.find_elements(By.CLASS_NAME,"esajLogout")) < 1:
                time.sleep(1)

            self.login = True  
        else:
            print("Logado")  

    def _CND_Estadual (self):  
        if not self._check_exists('_CND_ESTADUAL'):   
            self._navegador()
            try: 
                self.driver.get(config('PAGE_URL'))
                self._espera()
                self._existenciaPage("MainContent_txtDocumento")
                self.driver.execute_script(f"document.getElementById('MainContent_txtDocumento').value = '{self.dados.get('cpf')}'")
                c = Captcha(config('DATA_SITE_KEY'),config('PAGE_URL'))
                wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
                self.driver.execute_script(wirte_tokon_js)
                time.sleep(1)
                self.driver.find_element(By.ID,"MainContent_btnPesquisar").click()
                time.sleep(0.5)
                #VOU VERIFICAR SE EXISTE O BOTÂO DE IMPRIMIR NA TELA, SE SIM CLICK NELE
                self._existenciaItem("MainContent_btnImpressao")   
                self.driver.find_element(By.ID,"MainContent_btnImpressao").click()
                del c
                time.sleep(4)
                self._update_extract('_CND_ESTADUAL', self.dados.get('_id'))
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"ERRO _CND_ESTADUAL","msg_s":f"{e}"}
        else:
            return {"status":200, "msg":"Estadual - Já extraido","msg_s":""}        
                 

               

    def _CND_Municipal(self):
        if not self._check_exists('_CND_MUNICIPAL'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_MUN'))
                self._espera()
                self._existenciaPage("ctl00_ConteudoPrincipal_ddlTipoCertidao")

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
                #APAGAR OS ARQUIVOS GERADOS
                os.remove("page_"+str(namefile)+".png")
                os.remove("crop_"+str(namefile)+".png")

                self.driver.find_element(By.ID,"ctl00_ConteudoPrincipal_btnEmitir").click()
                                       
                time.sleep(6)
                try:
                    if self.driver.switch_to.alert.text.find("Conversion from string    to type 'Long' is not valid.") > -1:
                        c._report()
                        return {"status":404,"msg":"CND_MUNICIPAL - ERRO AO RESOLVER O RECAPTCHA","msg_s":"ERRO"} 
                except:
                    pass 

                del c    
                self._update_extract('_CND_MUNICIPAL', self.dados.get('_id'))
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"ERRO _CND_MUNICIPAL","msg_s":f"{e}"}  
        else:
            return {"status":200, "msg":"Municipal - Já extraido","msg_s":""}         
             

    def _CND_Contribuinte(self):
        if not self._check_exists('_CND_CONTRIBUINTE'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_CONTRIBUINTE'))
                self._espera()
                self._existenciaPage("emitirCrda:crdaInputCpf")
                self.driver.find_element(By.ID,"emitirCrda:crdaInputCpf").send_keys(self.dados.get('cpf'))
                c = Captcha(config('DATA_SITE_KEY_CONTRIBUINTE'),config('PAGE_URL_CONTRIBUINTE'))
                #print(f"Meu saldo atual é : {c._saldo()}.")
                wirte_tokon_js = f'document.getElementById("g-recaptcha-response").innerHTML="{c._resolve()}";'
                self.driver.execute_script(wirte_tokon_js)
                time.sleep(3)
                #self.driver.find_element(By.XPATH,"//*[@id='emitirCrda:j_id136_body']/div[2]/input[2]").click()
                self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div[2]/div[2]/span/form/div/div[2]/div[2]/input[2]").click()
                del c
                time.sleep(4)  
                self._update_extract('_CND_CONTRIBUINTE', self.dados.get('_id')) 
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"ERRO _CND_CONTRIBUINTE","msg_s":f"{e}"}  
        else:
            return {"status":200, "msg":"Contribuinte - Já extraido","msg_s":""}            
                        

    def _esaj_certidao(self,valor,prt_sc="1"):
        ret = {}
        if not self._check_exists(f'_ESAJ_CERTIDAO_{valor}'): 
            if not self.login:
                self._login_esaj()
                  
            try:
                   
                genero = self.dados.get("genero")
                self.driver.get(config('PAGE_URL_CRIMINAL_1'))
                self._espera()
                self._existenciaPage("cdModelo")
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

                time.sleep(2)

                while True:               
                    try:
                        self.driver.find_element(By.ID,"btnSim").click()
                        self.tentativas = 0
                        break
                    except:
                        if int(self.tentativas) < 3 :
                            self.tentativas += 1
                            time.sleep(1)
                            pass   
                        else:
                            break 

                time.sleep(6)

                if self.driver.page_source.find("Não foi possível executar esta operação. Tente novamente mais tarde.") > -1:
                    self.Erro = 1
                    ret = {"status":404,"msg":"ESAJ_CERTIDAO - Nao foi possivel executar esta operacao. Tente novamente mais tarde","msg_s":"ERRO"}
                else:
                    self._update_extract(f'_ESAJ_CERTIDAO_{valor}', self.dados.get('_id'))
                    ret = {"status":200,"msg":"CERTIDAO CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}

            except Exception as e:
                self.Erro = 1
                ret = {"status":404,"msg":f"ERRO _ESAJ_CERTIDAO_{valor}","msg_s":f"{e}"} 
        else:
            ret = {"status":200, "msg":f"Certidão {valor}- Já extraido","msg_s":""}         

        return ret

    def _trtsp(self):
        if not self._check_exists('_TRTSP'): 
            self._navegador()
            try:
                namefile = random.randrange(99999)
                self.driver.get(config('PAGE_URL_TRTSP'))
                self._espera()
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
                time.sleep(3)
                
                if self.driver.page_source.find("informado do captcha incorreto") > -1:
                    c._report()
                    #erro no recaptch

                os.remove("page_"+str(namefile)+".png")

                while True:
                    try:
                        if self.driver.page_source.find("Visualizar Certidão") > -1:
                            self.driver.find_element(By.XPATH,"//*[@id='main-content']/div/fieldset/button").click()
                            self.tentativas = 0
                            break
                        else:
                            if int(self.tentativas) < int(config('TENTATIVAS')):
                                self.tentativas += 1
                                time.sleep(2)
                                pass
                            else:
                                self.tentativas = 0  
                                self.Erro = 1         
                                return {"status":404,"msg":"ERRO _TRTSP","msg_s":"EXPIROU AS TENTATIVAS DE ABAIXAR O PDF"}         
                    except:

                        if int(self.tentativas) < int(config('TENTATIVAS')):
                            self.tentativas += 1
                            time.sleep(2)
                            pass
                        else:
                            self.tentativas = 0  
                            self.Erro = 1         
                            return {"status":404,"msg":"ERRO _TRTSP","msg_s":"EXPIROU AS TENTATIVAS DE ABAIXAR O PDF"}

                time.sleep(4) 
                self._update_extract('_TRTSP', self.dados.get('_id'))
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"ERRO _TRTSP","msg_s":f"{e}"}   
        else:
            return {"status":200, "msg":"TRTSP - Já extraido","msg_s":""}         
                  
    def _tst_trabalhista(self):
        if not self._check_exists('_TST_TRABALHISTA'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_TST'))
                self._espera()
                self._existenciaPage("corpo")
                self.driver.find_element(By.XPATH,"//*[@id='corpo']/div/div[2]/input[1]").click()

                while True:
                    try:
                        image_cap = self.driver.find_element(By.ID,"idImgBase64").get_attribute("src")
                        #print(image_cap.replace("data:image/png;base64, ",""))
                        if image_cap == None:
                            time.sleep(0.5)
                            pass
                        else:
                            break
                    except:
                        time.sleep(0.5)
                        pass 
                c = Captcha(image_cap,"")
                self.driver.find_element(By.ID,"gerarCertidaoForm:cpfCnpj").send_keys(self.dados.get('cpf'))
                self.driver.find_element(By.ID,"idCaptcha").send_keys(c._resolve_img())
                self.driver.find_element(By.ID,"gerarCertidaoForm:btnEmitirCertidao").click()
                time.sleep(5)
                
                if self.driver.page_source.find("Código de validação inválido.") > -1:
                    c._report()
                    self.Erro = 1
                    return {"status":404,"msg":"TST_TRABALHISTA - ERRO DE RECAPTCHA","msg_s":"ERRO"}

                del c
                self._update_extract('_TST_TRABALHISTA', self.dados.get('_id'))
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"_TST_TRABALHISTA","msg_s":f"{e}"}  
        else:
            return {"status":200, "msg":"Trabalhista - Já extraido","msg_s":""}         
            
    def __resolve_charada(self, texto):
        #resolve s charada do captcha
        sinal = ""
        valor_1 = ""
        valor_2 = ""
        for t in texto.strip():
            if t.isnumeric():
                if not sinal:
                    valor_1 += t
                else:
                    valor_2 += t
            if t != '=' and not t.isnumeric():
                sinal = t
        
        if valor_1:
            if sinal == "+":
                return int(valor_1) + int(valor_2)
            elif sinal == "-":
                return int(valor_1) - int(valor_2)
            elif sinal == "*":
                return int(valor_1) * int(valor_2)
            elif sinal == "/":
                return int(valor_1) / int(valor_2)

    def _trt15(self):
        if not self._check_exists('_TRT15'): 
            self._navegador()
            try:
                namefile = random.randrange(999999999)
                self.driver.get(config('PAGE_URL_TRT15'))
                self._espera()
                self._existenciaPage("certidaoActionForm:j_id23:doctoPesquisa")
                self.driver.find_element(By.ID,"certidaoActionForm:j_id23:doctoPesquisa").send_keys(self.dados.get('cpf'))

                self.driver.save_screenshot("page_"+str(namefile)+".png")
                a = Cut()
                #CROP ARQUIVO DE PRINT TELA, NOME DO ARQUIVO QUANDO CORTADO
                image_cap = a.crop("page_"+str(namefile)+".png","crop_"+str(namefile)+".png",215,250,62,132)
                c = Captcha(image_cap,"")
                texto_img = c._resolve_img()
                if texto_img.find('=') > -1:
                    texto_img = self.__resolve_charada(texto_img)

                self.driver.find_element(By.ID,"certidaoActionForm:j_id51:verifyCaptcha").send_keys(texto_img)
                self.driver.find_element(By.ID,"certidaoActionForm:certidaoActionEmitir").click()
                time.sleep(4)

                if self.driver.page_source.find("incorrect response") > -1:
                    c._report()
                    del c
                    del a
                    os.remove("page_"+str(namefile)+".png")
                    os.remove("crop_"+str(namefile)+".png")          
                    return {"status":404,"msg":"ERRO _TRT15 Recapactha nao resolvido","msg_s":"Problema ao resolver o captcha"}

                self._existenciaItem("certidaoActionForm:j_id12_body")
                self.driver.find_element(By.ID,"certidaoActionForm:certidaoActionImprimir").click()

                del c
                del a
                os.remove("page_"+str(namefile)+".png")
                os.remove("crop_"+str(namefile)+".png")

                time.sleep(4)
                self._update_extract('_TRT15', self.dados.get('_id'))
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except  Exception as e:
                self.Erro = 1
                return {"status":404,"msg":"ERRO _TRT15","msg_s":f"{e}"}  
        else:
            return {"status":200, "msg":"TRT15 - Já extraido","msg_s":""}         

    def _esaj_busca_nome_cpf(self,parm):
        if not self._check_exists(f'_ESAJ_BUSCA_{parm}'): 
            #self._navegador()
            try:
                if self.login == False:
                    self._login_esaj()
                    self._esaj_busca_nome_cpf(parm)
                else:
                    self.driver.get(config('PAGE_URL_ESAJ_B_NOME_CPF'))
                    self._espera()
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
                    time.sleep(6)
                    self._update_extract(f'_ESAJ_BUSCA_{parm}', self.dados.get('_id'))
                    return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.Erro = 1
                return {"status":404,"msg":f"ERRO _ESAJ_BUSCA_{parm}","msg_s":f"{e}"}        
        else:
            return {"status":200, "msg":f"Esaj {parm} Já extraido","msg_s":""}         

    def _protestos(self):
        if not self._check_exists('_PROTESTOS'): 
            self._navegador()
            try:
                self.driver.get(config('PAGE_URL_PROTESTO'))
                self._espera()
                self._existenciaPage("AbrangenciaNacional")
                try:
                    time.sleep(2)
                    self.driver.execute_script("document.getElementById('cookiefirst-root').style.display = 'none'")
                except:
                    pass
                self.driver.find_element(By.ID,"AbrangenciaNacional").click()
                self._select("TipoDocumento","1")
                self.driver.find_element(By.ID,"Documento").send_keys(self.dados.get('cpf'))
                self.driver.execute_script("ValidarConsulta(this)")
                time.sleep(4)

                if self._existenciaItem("resumoConsulta") == True:
                    pass
                else:
                    self.Erro = 1
                    self.driver.quit()
                    return {"status":404,"msg":"PROTESTO - TENTATIVAS ESGOTADAS","msg_s":"FALHA"}
                
                self.driver.execute_script('window.print();')
                time.sleep(4)
                self._update_extract('_PROTESTOS', self.dados.get('_id')) 
                #COMO ESSE CARA ELE E O ULTIMO VOU FAZER ELE FECHAR O BROWSER
                self.driver.quit()
                return {"status":200,"msg":"CONCLUIDO COM EXITO","msg_s":"SEM FALHAS NO SISTEMA"}
            except Exception as e:
                self.driver.quit()
                self.Erro = 1
                return {"status":404,"msg":"ERRO _PROTESTOS","msg_s":f"{e}"}   
        else:
            return {"status":200, "msg":"Protesto - Já extraido","msg_s":""}             
        
