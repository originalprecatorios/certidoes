# CERTIDÃO NEGATIVAS
from myclass.paginas import Paginas
from myclass.smtp import Smtp
from decouple import config
import time

cpf = "325.044.888-58"
p = Paginas(cpf)

p._CND_Estadual(cpf)
p._CND_Contribuinte(cpf)
p._CND_Municipal(cpf)
#p._CND_Federal(cpf)

#e = Smtp()
#e._Envia_Email("junior.ppp@gmail.com","Olá Gelson sua certidões foi extraidas com sucesso.")