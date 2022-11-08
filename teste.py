#!/usr/bin/python3


import pika, time, json


cp = ''

try:
    upload.creat('e-proc')
except:
    print ('Bucket já existe')

# Conecta no RabbitMQ para processar o que vier da queue "consumidor_gov"
class RabbitMQ:

   def __init__(self, pQueue):
      self._queue = pQueue
      self._host = '200.194.172.112'
      self._port = '5672'
      self._credentials = pika.PlainCredentials('robot', 'original2022!')
      
      self._conn = pika.BlockingConnection(pika.ConnectionParameters(host= self._host,port=self._port,credentials=self._credentials))
      self._channel = self._conn.channel()
      self._channel.queue_declare(queue=pQueue)


   def __dell__(self):
      self._channel.close()


   def send_queue(self, pBody):
      self._channel.basic_publish(exchange='', routing_key=self._queue, body=pBody)
      return True
    

   def get_queue(self):
      print('buscando')
      self._channel.queue_declare(queue=self._queue)
      retorno = self._channel.basic_get(queue=self._queue,auto_ack=True)

      # Fecha a conexão com o RabbitMQ
      self.__dell__()

      tem_dado = False
      if retorno[-1] != None:
         tem_dado = True

      return tem_dado, retorno[-1]
        

   def processa_dado(self, dados):

      dados['numero_cnj'] = dados['numero_cnj'].replace('.','').replace('-','').replace('/','')
      
      if dados['legado']:         

         exe = Eproc(mongo, dados['login'], dados['senha'], cp, dados['sistema'], upload, pLegado=True)
         exe.fazer_login()

         exe.ir_para_consulta_processual()
         exe.pesquisar_processo(dados['numero_cnj'])
         
      else:

         exe = Eproc(mongo, dados['login'], dados['senha'], cp, dados['sistema'], upload, pLegado=False)
         exe.fazer_login()

         exe.ir_para_consulta_processual()
         exe.pesquisar_processo(dados['numero_cnj'])


    
# Executa as filas do RabbitMQ
while True:

    rabbit = RabbitMQ('web_certidao')
    retorno = rabbit.get_queue()
    
    if retorno[0]:
        dados = json.loads(retorno[-1])
        rabbit.processa_dado(dados)
    else:
        time.sleep(300)





   

