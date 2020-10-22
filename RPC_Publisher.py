import pika
import uuid
import requests, random
import json
import time

class RpcClient(object):

    def __init__(self):
        self.credentials = pika.PlainCredentials("admin","0000")
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',credentials=self.credentials))
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', self.credentials, heartbeat=0))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response,
                                   auto_ack=True)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        #data = r.data
        #print('Enter call')
        '''if self.connection and not self.connection.is_closed:
            self.connection.close()
        if self.connection.is_closed:
            self.reconnect()'''
        while data :
            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(exchange='',
                                       routing_key='rpc_queue',
                                       properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                       correlation_id=self.corr_id,
                                                                       ),
                                       body=data)
            while self.response is None:
                self.connection.process_data_events()
            return self.response



credentials = pika.PlainCredentials("admin","0000")
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.4.184',credentials=credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters('172.24.4.100', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def forward_traffic(request_data):
    rpc = RpcClient()
    print(" [x] Requesting")
    response = rpc.call(request_data)
    return str(response.status_code)

def on_request(ch, method, props, body):
    #request = json.loads(body.decode())
    response = forward_traffic(body)#request)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=10)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
print(" [x] Awaiting RPC requests from Master Load Balancer")
channel.start_consuming()