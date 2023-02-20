#!/usr/bin/python3

from selenium_class.estadual import Estadual
from selenium_class.municipal import Municipal
from selenium_class.federal import Federal
from selenium_class.trt15 import Trt15
from selenium_class.distribuicao_federal import Distribuicao_federal
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
from selenium_class.esaj_busca import Esaj_busca
from create_certificate.create import Creat
from selenium_class.antecedentes_criminais import Antecedentes_criminais
from bd.class_mongo import Mongo
from decouple import config
from recaptcha.captcha import Solve_Captcha
from apscheduler.events import EVENT_JOB_ERROR
import time, os, json
from rabbit import rabbitmq
from bson.objectid import ObjectId
from crypto import db
import requests


        
def certidao_initial(id_mongo):
    print('Iniciando...')
    #bd = Mongo(config('MONGO_USER'), config('MONGO_PASS'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB'), config('AMBIENTE'))
    #mongo = Mongo(config('MONGO_USER'), config('MONGO_PASS'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB'), config('AMBIENTE'))
    mongo = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['MONGO_AUTH_DB_PROD'])
    #mongo = Mongo(config('MONGO_USER_PROD'), config('MONGO_PASS_PROD'), config('MONGO_HOST_PROD'), config('MONGO_PORT_PROD'), config('MONGO_DB_PROD'), config('MONGO_AUTH_DB_PROD'))
    erro = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], config('AMBIENTE_PROD'))
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
    
    if type(usr[0]['cpf']) is bytes:
        usr[0]['cpf'] = db.decrypt(usr[0]['cpf'])
    if type(user['rg']) is bytes:
        usr[0]['rg'] = db.decrypt(usr[0]['rg'])
    if usr[0]['rg'].find('.') >= 0:
        usr[0]['rg'] = usr[0]['rg'].replace('.','')   

    for u in usr:
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
                                logged = e.login()
                                if logged is True:
                                    e.download_document()
                                    del e
                                    modifica['$set']['extracted']['_CND_ESTADUAL'] = 1
                                    break
                                else:
                                    cont += 1
                                
                            except:
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
                            except:
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
                                f = Federal(u,os.environ['PAGE_URL_FEDERAL'],mongo,erro,u['cpf'])
                                f.login()
                                del f
                                modifica['$set']['extracted']['_CND_FEDERAL'] = 1
                                break
                            except:
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
                                df1 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'1','9- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA')
                                df1.login()
                                del df1
                                modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 1
                                break
                            except:
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
                                df2 = Distribuicao_federal(u,os.environ['PAGE_URL_TRF3_JUS'],mongo,erro,cap,u,'2','10- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA')
                                df2.login()
                                del df2
                                modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 1
                                break
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRF3_JUS_TRF')
                            break
                    
                
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
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_TRTSP'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _TRTSP')
                            break
                

                #elif ext == '_TRTSP':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                t = Trabalhista(u,cap,os.environ['PAGE_URL_TRTSP'])
                #                t.login()
                #                del t
                #                modifica['$set']['extracted']['_TRTSP'] = 1
                #                break
                #            except:
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_TRTSP'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _TRTSP')
                #            break
                    

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
                            except:
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
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PROTESTO'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PROTESTO')
                            break
                
                elif ext == '_PROTESTO2':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                p = Protesto2(u,os.environ['PAGE_URL_PROTESTO2'],mongo,erro,cap)
                                p.login()
                                del p
                                modifica['$set']['extracted']['_PROTESTO'] = 1
                                break
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PROTESTO'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PROTESTO')
                            break
                    
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
                            except:
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
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_CND_CONTRIBUINTE'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _CND_CONTRIBUINTE')
                            break
                    

                #elif ext == '_TJ':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                tj = Tj(u,os.environ['PAGE_URL_TJ'],mongo,erro,cap)
                #                tj.login()
                #                del tj
                #                modifica['$set']['extracted']['_TJ'] = 1
                #                break
                #            except:
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_TJ'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _TJ')
                #            break
                    
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
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_PJE_TRF3'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _PJE_TRF3')
                            break
                
                #elif ext == '_TST_TRABALHISTA':
                #    cont = 0
                #    while True:
                #        if cont <=2:
                #            try:
                #                tstt = Tst_trabalhista(u,os.environ['PAGE_URL_TST'],mongo,erro,cap)
                #                tstt.login()
                #                del tstt
                #                modifica['$set']['extracted']['_TST_TRABALHISTA'] = 1
                #                break
                #            except:
                #                cont += 1
                #        else:
                #            modifica['$set']['extracted']['_TST_TRABALHISTA'] = 2
                #            print('Erro ao acessar o site, para gerar a certidão _TST_TRABALHISTA')
                #            break
                

                elif ext == '_ESAJ_CERTIDAO_6':
                    cont = 0
                    while True:
                        if cont <=2:
                            try:
                                # email
                                e = Esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                e.get_data('6')
                                del e
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 1
                                break
                            except:
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
                                e = Esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                                e.login()
                                e.get_data('52')
                                del e
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 1
                                break
                            except:
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
                            except:
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
                            except:
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
                                c = Creat(u)
                                c.cert()
                                del c
                                modifica['$set']['extracted']['_PODER_JUDICIARIO'] = 1
                                break
                            except:
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
                            except:
                                cont += 1
                        else:
                            modifica['$set']['extracted']['_ANTECEDENTES_CRIMINAIS'] = 2
                            print('Erro ao acessar o site, para gerar a certidão _ANTECEDENTES_CRIMINAIS')
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

#dados = {'_id':'63efd8d819866cf6b78ac50c'}
#certidao_initial(dados)
# Executa as filas do RabbitMQ
while True:
    
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
        time.sleep(100)