import pika
import uuid
import requests, random
import json
import time
from flask import Flask, request
import threading


loadbalancer = Flask(__name__)

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


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        _credentials = pika.PlainCredentials("admin","0000")
        #connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.4.184',credentials=credentials))
        _connection = pika.BlockingConnection(pika.ConnectionParameters('172.24.4.100', 5672, '/', _credentials))
        _channel = _connection.channel()
        _channel.queue_declare(queue='rpc_queue')
        
        _channel.basic_qos(prefetch_count=10)
        _channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)
        print(" [x] Awaiting RPC requests from Master Load Balancer")
        _channel.start_consuming()

        
    def forward_traffic(self, request_data):
        url = 'http://localhost:5001'
        headers = {'X-M2M-Origin':'admin:admin', 'Content-Type':'application/xml;ty=4'}
        response = requests.post(url, data=request_data, headers=headers)
        #print(response.status_code)
        return str(response.status_code)

    def on_request(self, ch, method, props, body):
        #request = json.loads(body.decode())
        response = self.forward_traffic(body)#request)
        
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    

'''class Publisher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    @loadbalancer.route('/', methods=['POST','GET'])
    def handler(self):
        rpc = RpcClient()
        print(" [x] Requesting")
        response = rpc.call(request.data)
        #print(" [.] Got %r" % response)
        #print(" [.] Got %r" % request.data)
        return request.data
        
    def run(self):
        loadbalancer.run(host="127.0.0.1", port="5001")  '''      
        

@loadbalancer.route('/', methods=['POST','GET'])
def handler():
    rpc = RpcClient()
    print(" [x] Requesting")
    response = rpc.call(request.data)
    #print(" [.] Got %r" % response)
    #print(" [.] Got %r" % request.data)
    return request.data    



if __name__ == '__main__':
    thread_rcv = Consumer()
    thread_rcv.start()
    
    #thread_send = Publisher()
    #thread_send.start()
    loadbalancer.run(host="127.0.0.1", port="5001")
    