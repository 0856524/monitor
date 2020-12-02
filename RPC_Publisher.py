import pika
import uuid
from flask import Flask, request
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



loadbalancer = Flask(__name__)
#rpc = RpcClient()

@loadbalancer.route('/', methods=['POST','GET'])
def handler():
    rpc = RpcClient()
    #print(" [x] Requesting")
    response = rpc.call(request.data)
    #print(" [.] Got %r" % response)
    #print(" [.] Got %r" % request.data)
    return request.data

if __name__ == '__main__':
    loadbalancer.run(host="0.0.0.0")
