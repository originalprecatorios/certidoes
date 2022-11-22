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
    erro = Mongo(config('MONGO_USER_PROD'), config('MONGO_PASS_PROD'), config('MONGO_HOST_PROD'), config('MONGO_PORT_PROD'), config('MONGO_DB_PROD'), config('AMBIENTE_PROD'))
    mongo._getcoll('certidao')
    
    
    users  = mongo.returnQuery()
    cap = Solve_Captcha()
    usr = []
    list_process = []
    for user in users:
        usr.append(user)
    
    

    
    for u in usr:
      if type(u['cpf']) is bytes:
        u['cpf'] = db.decrypt(u['cpf'])
      if type(user['rg']) is bytes:
         u['rg'] = db.decrypt(u['rg'])
      print(u['rg'])
      if u['rg'] == '262.779.928-21':
         print()
      else:
         continue
      

dados = {'_id':'636e936ecd2cbfcfd5ad8511'}
certidao_initial(dados)
