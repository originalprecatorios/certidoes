#!/usr/bin/python3

from selenium_class.estadual import Estadual
from selenium_class.municipal import Municipal
from selenium_class.federal import Federal
from selenium_class.trt15 import Trt15
from selenium_class.distribuicao_federal import Distribuicao_federal
from selenium_class.debito_trabalhista import Debito_trabalhista
from selenium_class.protesto import Protesto
from request.trabalhista import Trabalhista
from request.federal_request import Federal_request
from request.divida_ativa import Divida_ativa
from selenium_class.tj import Tj
from selenium_class.trf import Trf
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
        e = Estadual(u,config('PAGE_URL'),mongo,erro,cap)
        logged = e.login()
        if logged is True:
            e.download_document()
   
        m = Municipal(u,config('PAGE_URL_MUN'),mongo,erro,cap)
        m.login()

        # USO COM O CHROME
        f = Federal(u,config('PAGE_URL_FEDERAL'),mongo,erro,u['cpf'])
        f.login()

        df1 = Distribuicao_federal(u,config('PAGE_URL_TRF3_JUS'),mongo,erro,cap,u,'1')
        df1.login()

        df2 = Distribuicao_federal(u,config('PAGE_URL_TRF3_JUS'),mongo,erro,cap,u,'2')
        df2.login()
        
        t = Trabalhista(u,cap)
        t.login()

        dt = Debito_trabalhista(u,config('PAGE_URL_DEBITO_TRABALHISTA'),mongo,erro,cap)
        dt.login()

        p = Protesto(u,config('PAGE_URL_PROTESTO'),mongo,erro,cap)
        p.login()

        t15 = Trt15(u,config('PAGE_URL_TRT15'),mongo,erro,cap)
        t15.login()

        da = Divida_ativa(u,cap)
        da.get_download()

        tj = Tj(u,config('PAGE_URL_TJ'),mongo,erro,cap)
        tj.login()

        trf = Trf(u,config('PAGE_URL_PJE_TRF3'),mongo,erro,cap)
        trf.login()

    print('Finalizando programa')