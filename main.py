#!/usr/bin/python3

from selenium_class.estadual import Estadual
from selenium_class.municipal import Municipal
from selenium_class.federal import Federal
from request.federal_request import Federal_request
from selenium_class.distribuicao_federal import Distribuicao_federal
from selenium_class.debito_trabalhista import Debito_trabalhista
from selenium_class.protesto import Protesto
from request.trabalhista import Trabalhista
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

        # USO COM O CHROME
        #e = Federal(u,config('PAGE_URL_FEDERAL'),mongo,erro,u['cpf'])
        #e.login()

        #d = Distribuicao_federal(u,config('PAGE_URL_TRF3_JUS'),mongo,erro,cap,u,'1')
        #d.login()

        #d = Distribuicao_federal(u,config('PAGE_URL_TRF3_JUS'),mongo,erro,cap,u,'2')
        #d.login()
        
        #t = Trabalhista(u,cap)
        #t.login()

        #d = Debito_trabalhista(u,config('PAGE_URL_DEBITO_TRABALHISTA'),mongo,erro,cap)
        #d.login()

        d = Protesto(u,config('PAGE_URL_PROTESTO'),mongo,erro,cap)
        d.login()
        

        
        
         

        '''
        cont = 0
        while True:
            if cont <= 5:
                try:
                    req = Federal_request(u['cpf'])
                    r = req.get_cookies()

                    e = Federal(u,config('PAGE_URL_FEDERAL'),mongo,erro,r,u['cpf'])
                    e.login()
                    break
                except:
                    cont += 1
                    continue
            else:
                break
        '''
    print('Finalizando programa')