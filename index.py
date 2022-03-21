# CERTIDÃO NEGATIVAS
from myclass.paginas import Paginas
from myclass.nodistill import Nodistill
#from myclass.smtp import Smtp
from db.class_mongo import Mongo
from decouple import config
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
import time,json,pytz

def _process():
    print("INICIALIZANDO PROCESSO...")
    mongo_datas = Mongo('certidoes')   
    mongo_datas._getcoll('dados_busca')
    datas = mongo_datas._return_query({'status_process':{'$exists':False}, 'process':{'$exists':False}})
    
    for data in datas:
        _id = data['_id']
        
        mongo_datas._update_one({'$set' : {'process':True}}, {'_id': _id})

        if 'extracted' not in data:

            mongo_datas._update_one({'$set' :{'extracted': {}}}, {'_id': _id})
            mongo_datas._update_one({'$set' :{'extracted': 
            {
                '_CND_ESTADUAL': False,
                '_CND_CONTRIBUINTE':False,
                '_CND_MUNICIPAL':False,
                '_CND_FEDERAL':False,
                '_TST_TRABALHISTA':False,
                '_TRTSP':False,
                '_TRT15':False,
                '_TRF3_JUS':False,
                '_ESAJ_CERTIDAO':False,
                '_ESAJ_BUSCA_NOME':False,
                '_ESAJ_BUSCA_CPF':False,
                '_PROTESTOS':False,
                '_PJE_TRF3':False
            }}}, {'_id': _id})

        p = Paginas(data)
        p._CND_Estadual()
        p._CND_Contribuinte()
        p._CND_Municipal()
        p._trtsp()
        p._tst_trabalhista()
        p._trt15()
        p._esaj_certidao()
        p._esaj_busca_nome_cpf("NOME")
        p._esaj_busca_nome_cpf("CPF")
        p._protestos()

        #PARTE DE DESTILL
        #pd = Nodistill(data)
        #pd._trf3_jus()
        #pd._pje_trf3(_cpf)
        #pd._CND_Federal()

        mongo_datas._update_one({'$set' :{'status_process': True}}, {'_id': _id})

#e = Smtp()
#e._Envia_Email("junior.ppp@gmail.com","Olá Gelson sua certidões foi extraidas com sucesso.")

executors = {
    'default': ThreadPoolExecutor(20),      
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    #DEFINE A QUANTIDADE DE INSTANCIAS QUE PODE TRABALHAR
    'max_instances': 1
}  
scheduler = BackgroundScheduler(
    executors=executors, job_defaults=job_defaults,
    timezone=pytz.timezone('America/Sao_Paulo')
)
#scheduler.add_job(_process, trigger='cron', hour='7')
scheduler.add_job(_process, 'interval', hours=1)

if __name__ == '__main__':  
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        #Isso faz com que não espere a conclusão da execução
        #scheduler.shutdown(wait=False)