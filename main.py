#!/usr/bin/python3

from selenium_class.estadual import Estadual
from selenium_class.municipal import Municipal
from selenium_class.federal import Federal
from selenium_class.trt15 import Trt15
#from selenium_class.distribuicao_federal import Distribuicao_federal
from request.distribuicao_federal import Distribuicao_federal
from selenium_class.debito_trabalhista import Debito_trabalhista
from selenium_class.protesto import Protesto
from selenium_class.protesto2 import Protesto2
#from request.trabalhista import Trabalhista
from selenium_class.trabalhista import Trabalhista
from request.federal_request import Federal_request
from selenium_class.divida_ativa import Divida_ativa
from selenium_class.tj import Tj
from selenium_class.trf import Trf
from selenium_class.tst_trabalhista import Tst_trabalhista
from selenium_class.esaj import Esaj
from request.request_esaj import Request_esaj
from selenium_class.esaj_busca import Esaj_busca
from create_certificate.create import Creat
from selenium_class.antecedentes_criminais import Antecedentes_criminais
from selenium_class.pje_trt import Pje_trt
from bd.class_mongo import Mongo
from decouple import config
from recaptcha.captcha import Solve_Captcha
from apscheduler.events import EVENT_JOB_ERROR
import time, os, json
from rabbit import rabbitmq
from bson.objectid import ObjectId
from crypto import db
import requests
from datetime import datetime
import subprocess

# Função utilizada para verificar se o chrome esta aberto gerando um numero de ID
# Caso esteja o mesmo espera 35 segundos e faz uma nova verificação
# se o numero de verificação do primeiro ID for igual ao segundo ID a função encerra o chrome
# Essa função é utilizado por um erro gerado nos sites FEDERAL, TRF3 e DISTRIBUIÇÂO FEDERAL quando abre 2 chrome do mesmo site
# quando abre 2 chrome com o mesmo site o google não carrega a página
def verifica_chrome():

    while True:
        process = subprocess.Popen(['pgrep', 'chrome'], stdout=subprocess.PIPE)
        output, error = process.communicate()

        # Armazena o ID do processo em uma variável
        chrome_process_id = output.decode('utf-8').strip()

        # Verifica se existe o ID do processo do Chrome
        if len(chrome_process_id) > 0 :
            
            process_id = chrome_process_id.split('\n')[0]
            time.sleep(35)

            process = subprocess.Popen(['pgrep', 'chrome'], stdout=subprocess.PIPE)
            output, error = process.communicate()

            chrome_process_id = output.decode('utf-8').strip()

            if len(chrome_process_id) > 0:
                process_id2 = chrome_process_id.split('\n')[0]
            else:
                process_id2 = ''
            
            if process_id2 == process_id:
                process = subprocess.Popen(['kill', process_id], stdout=subprocess.PIPE)
                output, error = process.communicate()
                break
            else:
                time.sleep(5)
                continue
        else:
            time.sleep(2)
            print('Não existe processo do chrome aberto')
            break

# Função que recebe do rabbit o numero do ID do mongo e quais certidoẽs baixar exempl: {"_id": "6405ec5128f620c3ddd9fb35", "certidao": "_TRT15"}
# Recebe a conexão do banco mongo e armazena em duas variaves 1 para oberter as informações necessárias para gerar as certidoes 2 para gerar log de erro
# Recebe os dados da collection certidao passando o id que foi recebido pelo rabbit
# Descriptografa o RG e o CPF
# Faz um looping com as certidoẽs que precisa ser baixada onde os dados foram informados pelo rabbit
# Baixa a certidão e muda o status no mongo caso gere erro o mesmo tenta 3 vezes gerar a certidão
# status 0: Solicitado baixa 1: Baixa concluida 2: Erro
# Salva os status na collection certidão e fecha as conexões do mongo
# Envia para o sistema B7 que o processo já foi realizado
def certidao_initial(id_mongo):
    print('Iniciando...')
    mongo = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['MONGO_AUTH_DB_PROD'])
    erro = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['MONGO_AUTH_DB_PROD'])
    mongo._getcoll('certidao')
    id = id_mongo['_id']
    arr = {
        "_id": ObjectId(id)
    }  
    users  = mongo.returnQuery(arr)
    cap = Solve_Captcha()
    usr = []
    list_process = []
    for user in users:
        usr.append(user)
    
    cpf_binario = usr[0]['cpf']
    
    if type(usr[0]['cpf']) is bytes:
        usr[0]['cpf'] = db.decrypt(usr[0]['cpf'])
    if type(user['rg']) is bytes:
        usr[0]['rg'] = db.decrypt(usr[0]['rg'])
    if usr[0]['rg'].find('.') >= 0:
        usr[0]['rg'] = usr[0]['rg'].replace('.','')   

    for u in usr:
        #for ext in id_mongo['certidao']:
        for ext in u['extracted']:
            busca = {'_id': u['_id']}
            modifica = {'$set' :{"extracted": {}}}
            modifica['$set']['extracted'] = u['extracted']
            if u['extracted'][ext] == 0:
                if ext == '_CND_ESTADUAL':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                e = Estadual(u,os.environ['PAGE_URL'],mongo,erro,cap)
                                logged,texto = e.login()
                                if logged is True:
                                    e.download_document()
                                    del e
                                    modifica['$set']['extracted']['_CND_ESTADUAL'] = 1
                                    break
                                else:
                                    if texto.find('Não foi possível emitir a Certidão Negativa.') >=0:
                                        modifica['$set']['extracted']['_CND_ESTADUAL'] = 2
                                        print('Não foi possível emitir a Certidão Negativa.')
                                        break
                                    if cont == 2:
                                        arr = {
                                            'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                            'error': texto,
                                            'cpf' : cpf_binario,
                                            'robot' : '_CND_ESTADUAL',
                                            'id_certidao': ObjectId(id),
                                        }
                                        erro.getcoll('error_cert')
                                        erro.addData(arr)
                                    cont += 1
                                
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_CND_ESTADUAL',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_CND_ESTADUAL'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _CND_ESTADUAL')
                            break
                    
                elif ext == '_CND_MUNICIPAL':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                m = Municipal(u,os.environ['PAGE_URL_MUN'],mongo,erro,cap)
                                m.login()
                                del m
                                modifica['$set']['extracted']['_CND_MUNICIPAL'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_CND_MUNICIPAL',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_CND_MUNICIPAL'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _CND_MUNICIPAL')
                            break
                    

                elif ext == '_CND_FEDERAL':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                # USO COM O CHROME
                                verifica_chrome()
                                f = Federal(u,os.environ['PAGE_URL_FEDERAL'],mongo,erro,u['cpf'])
                                resposta,texto = f.login()
                                if resposta is True:
                                    del f
                                    modifica['$set']['extracted']['_CND_FEDERAL'] = 1
                                    break
                                else:
                                    try:
                                        f._close()
                                    except:
                                        pass
                                    modifica['$set']['extracted']['_CND_FEDERAL'] = 2
                                    print('Certidão de Débitos Relativos a Créditos Tributários Federais e à Dívida Ativa da União\nResultado da Consulta\n\nAs informações disponíveis na Secretaria da Receita Federal do Brasil - RFB sobre o contribuinte 138.525.098-40 são insuficientes para a emissão de certidão por meio da Internet.\nPara consultar sua situação fiscal, acesse Centro Virtual de Atendimento e-CAC.\nPara maiores esclarecimentos, consulte a página Orientações para emissão de Certidão nas unidades da RFB.')
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': texto,
                                        'cpf' : cpf_binario,
                                        'robot' : '_CND_FEDERAL',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                    break

                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_CND_FEDERAL',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                                
                        else:
                            modifica['$set']['extracted']['_CND_FEDERAL'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _CND_FEDERAL')
                            break
                    
                
                elif ext == '_TRF3_JUS_SJSP':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                df1 = Distribuicao_federal(u,mongo,cap,'1','9- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CIVEL')
                                df1.initial()
                                retorno = df1.creat_html()
                                if retorno is True:
                                    df1.creat_document()
                                    del df1
                                    modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 1
                                    break
                                else:
                                    del df1
                                    modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 3
                                    break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_TRF3_JUS_SJSP',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRF3_JUS_SJSP')
                            break
                    

                elif ext == '_TRF3_JUS_TRF':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                df2 = Distribuicao_federal(u,mongo,cap,'2','10- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CIVEL')
                                df2.initial()
                                retorno = df2.creat_html()
                                if retorno is True:
                                    df2.creat_document()
                                    del df2
                                    modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 1
                                    break
                                else:
                                    del df2
                                    modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 3
                                    break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_TRF3_JUS_TRF',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRF3_JUS_TRF')
                            break
                

                elif ext == '_DISTRIBUICAO_FEDERAL_1_INSTANCIA':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                df1 = Distribuicao_federal(u,mongo,cap,'1','9.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CRIMINAL')
                                df1.initial()
                                retorno = df1.creat_html()
                                if retorno is True:
                                    df1.creat_document()
                                    del df1
                                    modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 1
                                    break
                                else:
                                    del df1
                                    modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 3
                                    break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_DISTRIBUICAO_FEDERAL_1_INSTANCIA',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _DISTRIBUICAO_FEDERAL_1_INSTANCIA')
                            break
                    

                elif ext == '_DISTRIBUICAO_FEDERAL_2_INSTANCIA':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                df2 = Distribuicao_federal(u,mongo,cap,'2','10.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CRIMINAL')
                                df2.initial()
                                retorno = df2.creat_html()
                                if retorno is True:
                                    df2.creat_document()
                                    del df2
                                    modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 1
                                    break
                                else:
                                    del df2
                                    modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 3
                                    break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_DISTRIBUICAO_FEDERAL_2_INSTANCIA',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _DISTRIBUICAO_FEDERAL_2_INSTANCIA')
                            break
                

                #elif ext == '_TRF3_JUS_SJSP':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                # USO COM O CHROME
                #                #verifica_chrome()
                #                df1 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'1','9- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CIVEL')
                #                df1.login()
                #                del df1
                #                modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 1
                #                break
                #            except Exception as e:
                #                if cont == 2:
                #                    arr = {
                #                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                #                        'error': str(e),
                #                        'cpf' : cpf_binario,
                #                        'robot' : '_TRF3_JUS_SJSP',
                #                        'id_certidao': ObjectId(id),
                #                    }
                #                    erro.getcoll('error_cert')
                #                    erro.addData(arr)
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _TRF3_JUS_SJSP')
                #            break
                    

                #elif ext == '_TRF3_JUS_TRF':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                # USO COM O CHROME
                #                #verifica_chrome()
                #                df2 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'2','10- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CIVEL')
                #                df2.login()
                #                del df2
                #                modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 1
                #                break
                #            except Exception as e:
                #                if cont == 2:
                #                    arr = {
                #                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                #                        'error': str(e),
                #                        'cpf' : cpf_binario,
                #                        'robot' : '_TRF3_JUS_TRF',
                #                        'id_certidao': ObjectId(id),
                #                    }
                #                    erro.getcoll('error_cert')
                #                    erro.addData(arr)
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _TRF3_JUS_TRF')
                #            break
                

                #elif ext == '_DISTRIBUICAO_FEDERAL_1_INSTANCIA':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                # USO COM O CHROME
                #                #verifica_chrome()
                #                df1 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'1','9.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CRIMINAL')
                #                df1.login()
                #                del df1
                #                modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 1
                #                break
                #            except Exception as e:
                #                if cont == 2:
                #                    arr = {
                #                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                #                        'error': str(e),
                #                        'cpf' : cpf_binario,
                #                        'robot' : '_DISTRIBUICAO_FEDERAL_1_INSTANCIA',
                #                        'id_certidao': ObjectId(id),
                #                    }
                #                    erro.getcoll('error_cert')
                #                    erro.addData(arr)
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _DISTRIBUICAO_FEDERAL_1_INSTANCIA')
                #            break
                    

                #elif ext == '_DISTRIBUICAO_FEDERAL_2_INSTANCIA':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                # USO COM O CHROME
                #                #verifica_chrome()
                #                df2 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'2','10.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CRIMINAL')
                #                df2.login()
                #                del df2
                #                modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 1
                #                break
                #            except Exception as e:
                #                if cont == 2:
                #                    arr = {
                #                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                #                        'error': str(e),
                #                        'cpf' : cpf_binario,
                #                        'robot' : '_DISTRIBUICAO_FEDERAL_2_INSTANCIA',
                #                        'id_certidao': ObjectId(id),
                #                    }
                #                    erro.getcoll('error_cert')
                #                    erro.addData(arr)
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _DISTRIBUICAO_FEDERAL_2_INSTANCIA')
                #            break
                    
                
                elif ext == '_TRTSP':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                t = Trabalhista(u,os.environ['PAGE_URL_TRTSP'],mongo,erro,cap)
                                t.login()
                                del t
                                modifica['$set']['extracted']['_TRTSP'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_TRTSP',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRTSP'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRTSP')
                            break
                

                elif ext == '_DEBITO_TRABALHISTA':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                dt = Debito_trabalhista(u,os.environ['PAGE_URL_DEBITO_TRABALHISTA'],mongo,erro,cap)
                                dt.login()
                                del dt
                                modifica['$set']['extracted']['_DEBITO_TRABALHISTA'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_DEBITO_TRABALHISTA',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_DEBITO_TRABALHISTA'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _DEBITO_TRABALHISTA')
                            break
                    

                elif ext == '_PROTESTO':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                p = Protesto(u,os.environ['PAGE_URL_PROTESTO'],mongo,erro,cap)
                                p.login()
                                del p
                                modifica['$set']['extracted']['_PROTESTO'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_PROTESTO',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PROTESTO'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PROTESTO')
                            break
                
                #elif ext == '_PROTESTO2':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                p = Protesto2(u,os.environ['PAGE_URL_PROTESTO2'],mongo,erro,cap)
                #                p.login()
                #                del p
                #                modifica['$set']['extracted']['_PROTESTO'] = 1
                #                break
                #            except Exception as e:
                #                if cont == 2:
                #                    arr = {
                #                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                #                        'error': str(e),
                #                        'cpf' : cpf_binario,
                #                        'robot' : '_PROTESTO',
                #                        'id_certidao': ObjectId(id),
                #                    }
                #                    erro.getcoll('error_cert')
                #                    erro.addData(arr)
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_PROTESTO'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _PROTESTO')
                #            break
                    
                elif ext == '_TRT15':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                t15 = Trt15(u,os.environ['PAGE_URL_TRT15'],mongo,erro,cap)
                                t15.login()
                                del t15
                                modifica['$set']['extracted']['_TRT15'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_TRT15',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRT15'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRT15')
                            break
                    
                
                elif ext == '_CND_CONTRIBUINTE':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                da = Divida_ativa(u,os.environ['PAGE_URL_CONTRIBUINTE'],mongo,erro,cap)
                                da.login()
                                del da
                                modifica['$set']['extracted']['_CND_CONTRIBUINTE'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_CND_CONTRIBUINTE',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_CND_CONTRIBUINTE'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _CND_CONTRIBUINTE')
                            break
                    
                    
                elif ext == '_PJE_TRF3':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                trf = Trf(u,os.environ['PAGE_URL_PJE_TRF3'],mongo,erro,cap)
                                trf.login()
                                del trf
                                modifica['$set']['extracted']['_PJE_TRF3'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_PJE_TRF3',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PJE_TRF3'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PJE_TRF3')
                            break
                

                elif ext == '_ESAJ_CERTIDAO_6':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                # email
                                e = Request_esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                e.solicita_arquivo('6')
                                e.verifica_pedido()
                                num_pedido,download =  e.download_arquivo('6')
                                del e
                                if download is True:
                                    modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 1
                                else:
                                    modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 3
                                if num_pedido is not True:
                                    mongo._upsert({'$set': {'data_pedido_6': num_pedido['data_pedido'], 'numero_pedido_6': num_pedido['numero_pedido']}}, {'_id': busca['_id']})
                                try:
                                    e.close_all()
                                except:
                                    pass
                                '''e = Esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                num_pedido = e.get_data('6')
                                del e
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 1
                                if num_pedido is not True:
                                    mongo._upsert({'$set': {'data_pedido_6': num_pedido['data_pedido'], 'numero_pedido_6': num_pedido['numero_pedido']}}, {'_id': busca['_id']})'''
                                break
                            except Exception as e:
                                try:
                                    e.close_all()
                                except:
                                    pass
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_ESAJ_CERTIDAO_6',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ESAJ_CERTIDAO_6')
                            break
                

                elif ext == '_ESAJ_CERTIDAO_52':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                # email
                                e = Request_esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                e.solicita_arquivo('52')
                                e.verifica_pedido()
                                num_pedido,download = e.download_arquivo('52')
                                del e
                                if download is True:
                                    modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 1
                                else:
                                    modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 3
                                if num_pedido is not True:
                                    mongo._upsert({'$set': {'data_pedido_52': num_pedido['data_pedido'], 'numero_pedido_52': num_pedido['numero_pedido']}}, {'_id': busca['_id']})
                                try:
                                    e.close_all()
                                except:
                                    pass
                                '''e = Esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                num_pedido = e.get_data('52')
                                del e
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 1
                                if num_pedido is not True:
                                    mongo._upsert({'$set': {'data_pedido_52': num_pedido['data_pedido'], 'numero_pedido_52': num_pedido['numero_pedido']}}, {'_id': busca['_id']})'''
                                break
                            except Exception as e:
                                try:
                                    e.close_all()
                                except:
                                    pass
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_ESAJ_CERTIDAO_52',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ESAJ_CERTIDAO_52')
                            break
                

                elif ext == '_ESAJ_BUSCA_CPF':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                e = Esaj_busca(u,os.environ['PAGE_URL_ESAJ_B_NOME_CPF'],mongo,erro,cap,'15- PESQUISA ONLINE TJSP - CPF')
                                e.login()
                                e.get_data('CPF')
                                del e
                                modifica['$set']['extracted']['_ESAJ_BUSCA_CPF'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_ESAJ_BUSCA_CPF',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ESAJ_BUSCA_CPF'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ESAJ_BUSCA_CPF')
                            break
                
                elif ext == '_ESAJ_BUSCA_NOME':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                e = Esaj_busca(u,os.environ['PAGE_URL_ESAJ_B_NOME_CPF'],mongo,erro,cap,'15.1- PESQUISA ONLINE TJSP - NOME')
                                e.login()
                                e.get_data('NOME')
                                del e
                                modifica['$set']['extracted']['_ESAJ_BUSCA_NOME'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_ESAJ_BUSCA_NOME',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ESAJ_BUSCA_NOME'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ESAJ_BUSCA_NOME')
                            break
                
                elif ext == '_PODER_JUDICIARIO':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                c = Creat(u,erro)
                                c.cert()
                                del c
                                modifica['$set']['extracted']['_PODER_JUDICIARIO'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_PODER_JUDICIARIO',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PODER_JUDICIARIO'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PODER_JUDICIARIO')
                            break
                
                elif ext == '_ANTECEDENTES_CRIMINAIS':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                ac = Antecedentes_criminais(u,os.environ['PAGE_URL_SSP'],mongo,erro,cap)
                                ac.login()
                                del ac
                                modifica['$set']['extracted']['_ANTECEDENTES_CRIMINAIS'] = 1
                                break
                            except Exception as e:
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_ANTECEDENTES_CRIMINAIS',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ANTECEDENTES_CRIMINAIS'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ANTECEDENTES_CRIMINAIS')
                            break
                
                elif ext == '_PJE_TRT':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                print('_PJE_TRT')
                                pj = Pje_trt(u,os.environ['PAGE_URL_PJE_TRT'],mongo,erro,cap)
                                print('abriu')
                                pj.login()
                                print('login')
                                del pj
                                modifica['$set']['extracted']['_PJE_TRT'] = 1
                                break
                            except Exception as e:
                                print(str(e))
                                if cont == 2:
                                    arr = {
                                        'created_at': str(datetime.today()).split(' ')[0].replace('-',''),
                                        'error': str(e),
                                        'cpf' : cpf_binario,
                                        'robot' : '_PJE_TRT',
                                        'id_certidao': ObjectId(id),
                                    }
                                    erro.getcoll('error_cert')
                                    erro.addData(arr)
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PJE_TRT'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PJE_TRT')
                            break
                    

        modifica['$set']['status_process'] = True
        mongo.updateOne_Query(busca, modifica)
    del mongo
    del erro

    headers = {

    # Already added when you pass json=

    # 'Content-Type': 'application/json',

    'Authorization': 'Bearer 2851F6E32BE3DFD959495AE626F589E3C16663E8334060BF7A126DD39612400B',

    }



    json_data = {

    'interests': [

        'User_{}'.format(u['iduser']),

    ],

    'web': {

        'notification': {

            'title': 'B7 Solutions',

            'body': 'As certdões do CPF {} já estão disponiveis no sistema.'.format(u['cpf']),

            'icon': 'http://localhost:8080/assets/images/b7-only-36x36.png'

                        },

        },

    }
    response = requests.post('https://f8f37533-9c29-482e-93e9-284804b874b7.pushnotifications.pusher.com/publish_api/v1/instances/f8f37533-9c29-482e-93e9-284804b874b7/publishes', headers=headers, json=json_data)
    print('Programa finalizado...')

# Configuração para teste

#dados = {'_id':'6467670e51f5f997fc86b340'}
#dados = {"_id": "6405ec5128f620c3ddd9fb35", "certidao": {"_TRT15"}}
#certidao_initial(dados)


# Executa a conexão com o Rabbit e armazena em uma variavel os dados existentes na fila
# Caso não tenha dados na fila o programa espera 3 minutos

while True:
    try:
        rabbit = rabbitmq.RabbitMQ(os.environ['RABBIT_QUEUE'])
        retorno = rabbit.get_queue()
        del rabbit
        if retorno[0]:
            try:
                dados = json.loads(retorno[-1])
            except:
                da = str(retorno[-1])
                dados = {
                    '_id':da.split(':')[1].split('"')[1]
                }
            certidao_initial(dados)
        else:
            time.sleep(60)
    except:
        print('Erro ao tentar conexão com o rabbit:')
        print('Tentando novamente em 60 segundos...')
        time.sleep(60)