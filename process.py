#!/usr/bin/python3

#from classRequest.stf import Stf
from request.distribuicao_federal import Distribuicao_federal
from bd.class_mongo import Mongo
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import pytz, time, os
from crypto import db
from recaptcha.captcha import Solve_Captcha
import datetime
from bson.objectid import ObjectId
from create_certificate.send_email import Email_enviar

def initial():
    data_atual = datetime.datetime.now()
    dias_somar = datetime.timedelta(days=7)
    data_passado = False
    mongo = Mongo(os.environ['MONGO_USER_PROD'], os.environ['MONGO_PASS_PROD'], os.environ['MONGO_HOST_PROD'], os.environ['MONGO_PORT_PROD'], os.environ['MONGO_DB_PROD'], os.environ['MONGO_AUTH_DB_PROD'])
    mongo._getcoll('certidao')
    arr = {
        'protocolo': { '$exists': True }
    }  
    users  = list(mongo.returnQuery(arr))

    cap = Solve_Captcha()
    
    for user in users:
        if user['created_at']+ dias_somar > data_atual:
            mongo._upsert({'$unset': {'protocolo': ''}}, {"_id": ObjectId(user['_id'])})
            data_passado = True
            

        if type(user['cpf']) is bytes:
            user['cpf'] = db.decrypt(user['cpf'])
        if type(user['rg']) is bytes:
            user['rg'] = db.decrypt(user['rg'])
        if user['rg'].find('.') >= 0:
            user['rg'] = user['rg'].replace('.','')   

        for ext in user['extracted']:
            busca = {'_id': user['_id']}
            modifica = {'$set' :{"extracted": {}}}
            modifica['$set']['extracted'] = user['extracted']
            if user['extracted'][ext] == 3:
                if data_passado is True:
                    user['extracted'][ext] = 2
                    smtp_config = {'host': os.environ['SMTP_SERVE'], 'port': os.environ['SMTP_PORT'], 'user': os.environ['SMTP_USER'], 'passwd':os.environ['SMTP_PASS']}
                    e = Email_enviar(os.environ['SMTP_USER'],'@#$WSDEqasw1!','',[user['email']],smtp_config)
                    texto = """O Prazo de 5 dias expirou, não foi possivel obter o certificado {} para o cliente {}""".format(ext,user['nome'])
                    e.send_email_ruralservice('',texto)
                    break

                if ext == '_TRF3_JUS_SJSP':
                                    
                    df1 = Distribuicao_federal(user,mongo,cap,'1','9- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CIVEL')
                    retorno = df1.imprimir()
                    if retorno is True:
                        df1.creat_document()
                        df1.email(ext)
                        del df1
                        modifica['$set']['extracted']['_TRF3_JUS_SJSP'] = 1
                        break
                                        
                elif ext == '_TRF3_JUS_TRF':
                    
                    df2 = Distribuicao_federal(user,mongo,cap,'2','10- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CIVEL')
                    retorno = df2.imprimir()
                    if retorno is True:
                        df2.creat_document()
                        df2.email(ext)
                        del df2
                        modifica['$set']['extracted']['_TRF3_JUS_TRF'] = 1
                        break
                                
                elif ext == '_DISTRIBUICAO_FEDERAL_1_INSTANCIA':
                    
                    df1 = Distribuicao_federal(user,mongo,cap,'1','9.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 1ª INSTANCIA','CRIMINAL')
                    retorno = df1.imprimir()
                    if retorno is True:
                        df1.creat_document()
                        df1.email(ext)
                        del df1
                        modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_1_INSTANCIA'] = 1
                        break
                                
                elif ext == '_DISTRIBUICAO_FEDERAL_2_INSTANCIA':
                    
                    df2 = Distribuicao_federal(user,mongo,cap,'2','10.1- CERTIDÃO DE DISTRIBUIÇÃO FEDERAL DE 2ª INSTANCIA','CRIMINAL')
                    retorno = df2.imprimir()
                    if retorno is True:
                        df2.creat_document()
                        df2.email(ext)
                        del df2
                        modifica['$set']['extracted']['_DISTRIBUICAO_FEDERAL_2_INSTANCIA'] = 1
                        break

        mongo.updateOne_Query(busca, modifica)
                       
    del mongo


    print('programa finalizado')
initial()
executors = {
    'default': ThreadPoolExecutor(20),      
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
    
scheduler = BackgroundScheduler(
    executors=executors, job_defaults=job_defaults,
    timezone=pytz.timezone('America/Sao_Paulo')
)

scheduler.add_job(initial, trigger='cron', hour='7')

if __name__ == '__main__':  
    print('Start')
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()