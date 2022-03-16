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
    mongo = Mongo('original')
    mongo_datas = Mongo('certidoes')   
    mongo_datas._getcoll('dados_busca')
    datas = mongo_datas._return_query({'status_process':{'$exists':False}})

    #mongo_datas._update_one({'$set' :{'extracted':{'TRF': True,'data':'16/03/2020'}}}, {'_id': _id})
    
    for data in datas:
        _id = data['_id']
        _cpf = data['cpf']

        p = Paginas(_cpf)
        p._CND_Estadual(_cpf)
        p._CND_Contribuinte(_cpf)
        p._CND_Municipal(_cpf)
        #p._trtsp(data)
        p._tst_trabalhista(_cpf)
        p._trt15(_cpf)
        #p._trf3_jus(dados)
        p._esaj_certidao(data)
        p._esaj_busca_nome_cpf(data,"nome")
        p._esaj_busca_nome_cpf(data,"cpf")
        p._protestos(data)

        #PARTE DE DESTILL
        pd = Nodistill(_cpf)
        #pd._pje_trf3(_cpf)
        pd._CND_Federal(_cpf)


        mongo_datas._update_one({'$set' :{'status_process': True}}, {'_id': _id})


#e = Smtp()
#e._Envia_Email("junior.ppp@gmail.com","Olá Gelson sua certidões foi extraidas com sucesso.")

#pd = Nodistill("325.044.888-58")
#pd._CND_Federal("325.044.888-58")
_process()