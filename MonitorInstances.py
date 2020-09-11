import os
import time
from subprocess import check_output
from subprocess import check_output
import socket

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips.decode())
#ip = ip[2:-4]
ip = ip.split(' ')[0]
#print(len(ip))
print("Instances's IP:", ip)

while True:
    '''CPU_output = str(os.popen('dstat -c 1 1').readlines())
    output = CPU_output.split(' ')
    CPU_Pct = 0
    cnt = 0
    # print(' +++ ')
    for item in output:
        if len(item) <= 3 and len(item) != 0 and cnt < 2:
            # print(item)
            CPU_Pct += int(item)
            cnt += 1'''

    CPU_Pctn = os.popen("""top -b -n2 | grep "Cpu(s)" | awk '{print $2+$4}' | tail -n1""").readline()
    CPU_Pct = CPU_Pctn.split('\n')[0]
    

    # print results
    mem = str(os.popen('free -t -m').readlines())

    T_ind = mem.index('M')

    mem_G = mem[T_ind + 14:-4]
    Total_mem = mem_G.split()[0]
    Used_mem = mem_G.split()[1]
    mem_U_in_Percent = (int(Used_mem) / int(Total_mem)) * 100
    mem_U_in_Percent = round(mem_U_in_Percent, 2)
    print("*******************************")
    print("CPU Usage = " + str(CPU_Pct), "%")
    print("Total mem:", Total_mem, "Mb")
    print("Used mem:", Used_mem, "Mb")
    print('Mem usage in percent:', mem_U_in_Percent, "%")
    print("*******************************")

    # time.sleep(1)
    '''# print(type(CPU_Pct))
    payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
    r = requests.post('http://192.168.122.190:9999/Instances', data=payload)
    # print("<Response [{a}]>".format(a=r.status_code))
    print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))'''

    server_host = "192.168.1.197"
    server_port = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    message = "ip:"+ip+" cpu_pct:"+ str(CPU_Pct)
    client.send(message.encode())
    response = client.recv(4096)
    print(response.decode())
