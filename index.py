# CERTIDÃO NEGATIVAS
from myclass.paginas import Paginas
from myclass.nodistill import Nodistill
from myclass.smtp import Smtp
from db.class_mongo import Mongo
from decouple import config
import time,json

#MODELOS apenas para esaj certificdo
#6 - CERTIDÃO DE DISTRIBUIÇÃO DE AÇÕES CRIMINAIS

def _process():
    #mongo = Mongo('original')
    mongo_datas = Mongo('certidoes')   
    mongo_datas._getcoll('dados_busca')
    datas = mongo_datas._return_query({'status_process':{'$exists':False}})
    
    for data in datas:
        _id = data['_id']

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
        #p._trtsp(data)
        p._tst_trabalhista()
        p._trt15()
        #p._trf3_jus(dados)
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

#pd = Nodistill("325.044.888-58")
#pd._CND_Federal("325.044.888-58")

#mongo_datas = Mongo('certidoes')
#mongo_datas._update_one({'$pull' :{'extracted':{'TRF': True,'data':'16/03/2020'}}}, {'_id': object("6230f2c58016eeeba8ce9f34")})

_process()