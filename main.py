#!/usr/bin/python3

from selenium_class.estadual import Estadual
from selenium_class.municipal import Municipal
from selenium_class.federal import Federal
from request.federal_request import Federal_request
from bd.class_mongo import Mongo
from decouple import config
from recaptcha.solve_captcha import hCaptcha
from recaptcha.captcha import Solve_Captcha

if __name__ == '__main__':
    #bd = Mongo(config('MONGO_USER'), config('MONGO_PASS'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB'), config('AMBIENTE'))
    #mongo = Mongo(config('MONGO_USER'), config('MONGO_PASS'), config('MONGO_HOST'), config('MONGO_PORT'), config('MONGO_DB'), config('AMBIENTE'))

    mongo = Mongo(config('MONGO_USER_PROD'), config('MONGO_PASS_PROD'), config('MONGO_HOST_PROD'), config('MONGO_PORT_PROD'), config('MONGO_DB_PROD'), config('AMBIENTE_PROD'))
    erro = Mongo(config('MONGO_USER_PROD'), config('MONGO_PASS_PROD'), config('MONGO_HOST_PROD'), config('MONGO_PORT_PROD'), config('MONGO_DB_PROD'), config('AMBIENTE_PROD'))
    mongo._getcoll('dados_busca')
    users  = mongo.returnQuery()
    cap = Solve_Captcha()
    usr = []
    list_process = []
    for user in users:
        usr.append(user)
    
    
    for u in usr:
        #e = Estadual(u,config('PAGE_URL'),mongo,erro,cap)
        #logged = e.login()
        #if logged is True:
        #    e.download_document()
   
        #e = Municipal(u,config('PAGE_URL_MUN'),mongo,erro,cap)
        #e.login()
        while True:
            req = Federal_request()
            r = req.get_cookies()
        e = Federal(u,config('PAGE_URL_FEDERAL'),mongo,erro,r)
        e.login()
        
    print('Finalizando programa')