import pika, time, json, os

# Conecta no RabbitMQ"
class RabbitMQ:

    def __init__(self, pQueue):
        self._queue = pQueue
        self._host = os.environ['RABBIT_HOST']
        self._port = os.environ['RABBIT_PORT']
        self._credentials = pika.PlainCredentials(os.environ['RABBIT_USR'], os.environ['RABBIT_PWD'])

        self._conn = pika.BlockingConnection(pika.ConnectionParameters(host=self._host, port=self._port, credentials=self._credentials))
        self._channel = self._conn.channel()

        # Declara uma nova fila para verificar suas propriedades
        result = self._channel.queue_declare(queue='', durable=False)

        if not result.method.queue:
            print(f"A fila '{pQueue}' não existe.")
        else:
            if result.method.queue != pQueue:
                print(f"A fila '{pQueue}' já existe com a propriedade 'durable' definida como True.")
            else:
                print(f"A fila '{pQueue}' já existe com a propriedade 'durable' definida como False.")


    def __dell__(self):
        self._channel.close()


    def send_queue(self, pBody):
        self._channel.basic_publish(exchange='', routing_key=self._queue, body=pBody)
        return True
    

    def get_queue(self):
        print('buscando')
        retorno = self._channel.basic_get(queue=self._queue, auto_ack=True)

        # Fecha a conexão com o RabbitMQ
        self.__dell__()

        tem_dado = False
        if retorno[-1] is not None:
            tem_dado = True

        return tem_dado, retorno[-1]