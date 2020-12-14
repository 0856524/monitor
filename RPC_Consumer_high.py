import pika
import json
import random
import requests
import socket
import time
import sys

'''bind_port = 8888
bind_ip = "0.0.0.0"
max_ins = 3
lb_ip = '172.24.4.'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(100)
print("Listening on {ip}:{port}".format(ip=bind_ip, port=bind_port))

while True:
    #while self.print_info_flag == 1:
    #    pass    
    #self.print_info_flag = 1
    client, addr = server.accept()
    #print(" ++ Accepted connection from: {ip}:{port}".format(ip=addr[0].decode(), port=addr[1]))
    request = client.recv(1024)
    ins_no = request.decode().split('.')[1]
    message = 'ACK.'
    client.send(message.encode())
    client.close()
    server.close()
    break
    
print(ins_no)
lb_ip = lb_ip + str(int(200+((int(ins_no)-1)/max_ins)+1))'''

lb_ip = '172.24.4.' + str(int(600+int(sys.argv[1])))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',8080))
while result != 0:
    result = sock.connect_ex(('127.0.0.1',8080))
    #if result == 0:
        #print("Port is open")
        #break
    #else:
        #print("Port is not open")
        #continue
print("Port is open")
time.sleep(10)

credentials = pika.PlainCredentials("admin","0000")
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.4.184',credentials=credentials))
connection = pika.BlockingConnection(pika.ConnectionParameters(lb_ip, 5672, '/', credentials))
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

channel.basic_qos(prefetch_count=5)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
print(" [x] Awaiting RPC requests")
channel.start_consuming()
