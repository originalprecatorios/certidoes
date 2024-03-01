import pika, time, json, os

# Conecta no RabbitMQ"
class RabbitMQ:

    def __init__(self, pQueue):
        self._queue = pQueue
        self._host = os.getenv('RABBIT_HOST')
        self._port = os.getenv('RABBIT_PORT')
        self._credentials = pika.PlainCredentials(os.getenv('RABBIT_USR'), os.getenv('RABBIT_PWD'))

        #self._host = 'localhost'
        #self._port = '5672'
        #self._credentials = pika.PlainCredentials('guest', 'guest')
        
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