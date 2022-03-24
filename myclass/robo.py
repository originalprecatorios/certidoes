# CERTIDÃO NEGATIVAS
from myclass.paginas import Paginas
from myclass.nodistill import Nodistill
#from myclass.smtp import Smtp
from db.class_mongo import Mongo
from decouple import config

class Robo:
    def __init__(self):
        pass
    
    def _process(self):
        print("INICIALIZANDO PROCESSO...")
        mongo_datas = Mongo('certidoes')   
        mongo_datas._getcoll('dados_busca')
        datas = mongo_datas._return_query({'status_process':{'$exists':False}, 'process':{'$exists':False}})
        
        for data in datas:
            _id = data['_id']
            _cpf = data['cpf']
            
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
                    '_TRF3_JUS_TRF':False,
                    '_TRF3_JUS_SJSP':False,
                    '_ESAJ_CERTIDAO_6':False,
                    '_ESAJ_CERTIDAO_52':False,
                    '_ESAJ_BUSCA_NOME':False,
                    '_ESAJ_BUSCA_CPF':False,
                    '_PROTESTOS':False,
                    '_PJE_TRF3':False
                }}}, {'_id': _id})

            p = Paginas(data)
            """
            Esaj Certidão
            string - Numero do id Modelo
            Boolean - 0 (Não tira screenshot da tela), por padrão é 1
            """
            p._esaj_certidao('6',"0")
            p._esaj_certidao('52',"0")
            p._esaj_busca_nome_cpf("NOME")
            p._esaj_busca_nome_cpf("CPF")

            p._CND_Estadual()
            p._CND_Contribuinte()
            p._CND_Municipal()
            p._trtsp()
            p._tst_trabalhista()
            p._trt15()            
            p._protestos()

            #PARTE DE DESTILL
            pd = Nodistill(data)
            pd._CND_Federal()
            pd._trf3_jus('TRF')
            pd._trf3_jus('SJSP')

            

            #pd._pje_trf3(_cpf)

            #CASO OUVER ALGUM ERRO NÂO ATUALIZA STATUS_PROCESS E PROCESS
            if p.Erro == 1 or pd.Erro == 1:
                mongo_datas._update_one({'$set' : {'process':False}}, {'_id': _id})
                dt = mongo_datas._return_query({'_id':_id},{'extracted':1})

                arq = open(config('PATH_FILES')+_cpf+"/resumo.txt","a")

                for chave,d in dt:
                    arq.write(str(d) + " - " + chave)
                    false - _CND_ESAJ
                    TRUE - PJE

                arq.close()

            else:
                mongo_datas._update_one({'$set' :{'status_process': True}}, {'_id': _id})

               
        #e = Smtp()
        #e._Envia_Email("junior.ppp@gmail.com","Olá Gelson sua certidões foi extraidas com sucesso.")