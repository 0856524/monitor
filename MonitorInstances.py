import os
import time
import requests
from subprocess import check_output
from subprocess import check_output

ips = check_output(['hostname', '--all-ip-addresses'])
ip = str(ips)
ip = ip[2:-4]
print(len(ip))
print("Instances's IP:", ip)

while True:
    CPU_Pct = str(round(float(
        os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),
                        2))

    # print results
    mem = str(os.popen('free -t -m').readlines())

    T_ind = mem.index('M')

    mem_G = mem[T_ind + 14:-4]
    Total_mem = mem_G.split()[0]
    Used_mem = mem_G.split()[1]
    mem_U_in_Percent = (int(Used_mem) / int(Total_mem)) * 100
    mem_U_in_Percent = round(mem_U_in_Percent, 2)
    print("*******************************")
    print("CPU Usage = " + CPU_Pct, "%")
    print("Total mem:", Total_mem, "Mb")
    print("Used mem:", Used_mem, "Mb")
    print('Mem usage in percent:', mem_U_in_Percent, "%")
    print("*******************************")
    time.sleep(1)
    # print(type(CPU_Pct))
    payload = "{ip}, {CPU_Pct}".format(ip=ip, CPU_Pct=CPU_Pct)
    r = requests.post('http://192.168.1.197:9999/Instances', data=payload)
    # print("<Response [{a}]>".format(a=r.status_code))
    print("<Response [{status_code}] {reason}>".format(status_code=r.status_code, reason=r.reason))