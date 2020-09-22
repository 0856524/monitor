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
start_time = time.time()
while True:
    '''CPU_Pctn = os.popen("""top -b -n2 | grep "Cpu(s)" | awk '{print $2+$4}' | tail -n1""").readline()
    CPU_Pct = CPU_Pctn.split('\n')[0]

    print("Total mem:" + Total_mem + " Mb")
    print("Used mem:" + Used_mem + " Mb")
    print('Mem usage in percent:' + str(mem_Pct) + "%")mem = str(os.popen('free -t -m').readlines())
    get_mem = mem.split()
    Total_mem = get_mem[8]
    Used_mem = get_mem[9]
    mem_Pct = (float(Used_mem)/float(Total_mem))*100
    mem_Pct = round(mem_Pct, 2)'''

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
    '''# print(type(CPU_Pct))
    payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
    r = requests.post('http://192.168.122.190:9999/Instances', data=payload)
    # print("<Response [{a}]>".format(a=r.status_code))
    print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))'''

    server_host = "192.168.1.197"
    server_port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    message = "ip:"+ip + " cpu_pct:"+str(CPU_Pct) + " mem_pct:"+str(mem_Pct)
    client.send(message.encode())
    response = client.recv(4096)
    print(response.decode())
    
    '''floating_ip = response.decode().split('/')[1]
    #print('floating IP = '+floating_ip)
    
    url = 'http://'+floating_ip+':8080/webpage'
    if init_flag == 0 and (time.time()-start_time)>=80:
        r = requests.get(url)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            init_flag = 1

            cmd = 'curl -X POST -H "X-M2M-Origin : admin:admin" -H "Content-Type: application/xml;ty=2" --data "@./data_app.xml" http://'+floating_ip+':8080/~/in-cse'
            os.system(cmd)
            time.sleep(1)
            cmd = 'curl -X POST -H "X-M2M-Origin : admin:admin" -H "Content-Type: application/xml;ty=3" --data "@./data_container.xml" http://'+floating_ip+':8080/~/in-cse/in-name/MY_SENSOR'
            os.system(cmd)'''
    
