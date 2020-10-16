import pika
import json
import random
import requests
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',8080))
while result != 0:
    pass
    #if result == 0:
        #print("Port is open")
        #break
    #else:
        #print("Port is not open")
        #continue

credentials = pika.PlainCredentials("admin","0000")
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.4.184',credentials=credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters('172.24.4.100', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def forward_traffic(request_data):
    url = 'http://localhost:8080/~/in-cse/in-name/SENSOR/DATA'
    headers = {'X-M2M-Origin':'admin:admin', 'Content-Type':'application/xml;ty=4'}
    response = requests.post(url, data=request_data, headers=headers)
    #print(response.status_code)
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

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
print(" [x] Awaiting RPC requests")
channel.start_consuming()
