#!/usr/bin/python3
from request.request_esaj_reprocess import Request_esaj
from bd.class_mongo import Mongo
from decouple import config
from recaptcha.captcha import Solve_Captcha
from apscheduler.events import EVENT_JOB_ERROR
import time, os, json
from rabbit import rabbitmq_reprocess
from bson.objectid import ObjectId
from crypto import db
import requests
from datetime import datetime
import subprocess


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
            
            if id_mongo['certidao'] == '_ESAJ_CERTIDAO_6':
                cont = 0
                while True:
                    if cont <=2:
                        try:
                            # email
                            e = Request_esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                            e.login()
                            download =  e.download_arquivo('6')
                            if download is True:
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 1
                            else:
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_6'] = 2
                            try:
                                e.close_all()
                            except:
                                pass
                            
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
                break

            elif id_mongo['certidao'] == '_ESAJ_CERTIDAO_52':
                cont = 0
                while True:
                    if cont <=2:
                        try:
                            # email
                            e = Request_esaj(u,os.environ['PAGE_URL_CRIMINAL_1'],mongo,erro,cap)
                            e.login()
                            download = e.download_arquivo('52')
                            if download is True:
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 1
                            else:
                                modifica['$set']['extracted']['_ESAJ_CERTIDAO_52'] = 2
                            try:
                                e.close_all()
                            except:
                                pass
                            
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
#dados = {'_id': '6478d18dac1497d37eb3e081', 'certidao': '_ESAJ_CERTIDAO_52'}
#certidao_initial(dados)


# Executa a conexão com o Rabbit e armazena em uma variavel os dados existentes na fila
# Caso não tenha dados na fila o programa espera 3 minutos

while True:
    try:
        rabbit = rabbitmq_reprocess.RabbitMQ('reprocesso_52_6')
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