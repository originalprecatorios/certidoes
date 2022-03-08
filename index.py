# CERTIDÃO NEGATIVAS
from myclass.paginas import Paginas
from myclass.smtp import Smtp
from decouple import config
import time,json

#MODELOS apenas para esaj certificdo
#6 - CERTIDÃO DE DISTRIBUIÇÃO DE AÇÕES CRIMINAIS
dados = {'modelo':'6', 'cpf': '325.044.888-58', 'rg' : '336343255', 'nascimento':'08/04/1983', 'nome': 'Gelson Luiz Ramos Pereira Junior', 'genero' : 'M', 'mae' : 'Teresinha Lucia da Costa Ramos Pereira'}

p = Paginas(dados.get('cpf'))

p._CND_Estadual(dados.get('cpf'))
p._CND_Contribuinte(dados.get('cpf'))
p._CND_Municipal(dados.get('cpf'))
#p._CND_Federal(dados.get('cpf'))
#p._login_esaj()
#time.sleep(100)

#MODELOS
p._esaj_certidao(dados)
p._trtsp(dados)
e = Smtp()
e._Envia_Email("junior.ppp@gmail.com","Olá Gelson sua certidões foi extraidas com sucesso.")