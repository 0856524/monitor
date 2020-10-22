import os
import time
from subprocess import check_output
from subprocess import check_output
import socket
import requests
import psutil

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips.decode())
#ip = ip[2:-4]
ip = ip.split(' ')[0]
#print(len(ip))
print("Instances's IP: " + ip)


init_flag = 0
while True:

    CPU_Pct = psutil.cpu_percent()
    Total_mem = psutil.virtual_memory().total
    Used_mem = psutil.virtual_memory().used
    mem_Pct = (float(Used_mem)/float(Total_mem))*100
    mem_Pct = round(mem_Pct, 2)    
    
    print("*******************************")
    print("CPU Usage = " + str(CPU_Pct) + "%")
    print("Total mem:" + str(Total_mem/(1024*1024)) + " Mb")
    print("Used mem:" + str(Used_mem/(1024*1024)) + " Mb")
    print('Mem usage in percent:' + str(mem_Pct) + "%")
    print("*******************************")

    time.sleep(1)

    server_host = "192.168.1.197"
    server_port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    message = "ip:"+ip + " cpu_pct:"+str(CPU_Pct) + " mem_pct:"+str(mem_Pct)
    client.send(message.encode())
    response = client.recv(4096)
    print(response.decode())
    
    if init_flag == 0:
        count_str = response.decode().split('/')[1]
        server_host2 = "127.0.0.1"
        server_port2 = 8888
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect((server_host2, server_port2))
        message = "No." + count_str
        client2.send(message.encode())
        response = client2.recv(4096)
        print(response.decode())
        init_flag = 1

