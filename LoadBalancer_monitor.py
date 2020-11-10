from flask import Flask, request
import requests
import json
import os


ns_num = 0
il_status = 0
path_conf = './default.conf'
path_new_conf = './default_tmp.conf'
              

loadbalancer = Flask(__name__)
@loadbalancer.route('/', methods=['POST','GET'])
def handler():
    global ns_num
    global il_status
    global path_conf
    global path_new_conf

    # Get information from master node
    print(" [x] Requesting")
    get_data = request.data.decode()
    get_ns_num = int(json.loads(get_data)['ns_num'])
    get_il_status_num = int(json.loads(get_data)['il_status_num'])
    get_il_max = int(json.loads(get_data)['il_max'])
    #print(str(get_ns_num))
    #print(str(get_il_status))
    
    # If status change
    if ns_num!=get_ns_num or il_status!=get_il_status_num:
        # Modify and create the new default
        fpr = open(path_conf, "r")
        fpw = open(path_new_conf, "w")
        line = fpr.readline()
        while line:
            if 'server 172.24.4.201:5000' in line:
                for cnt in range(get_ns_num):
                    if cnt+1 == get_ns_num:
                        line = '    server 172.24.4.20' + str(cnt+1) + ':5000 weight=' + str(get_il_status_num) + ';\n'
                    else:
                        line = '    server 172.24.4.20' + str(cnt+1) + ':5000 weight=' + str(get_il_max) + ';\n'
                    fpw.writelines(line)
                line = fpr.readline()
            elif 'server 172.24.4.2' in line:
                line = fpr.readline()
            else:
                fpw.writelines(line)
                line = fpr.readline()
        ns_num = get_ns_num
        il_status = get_il_status_num
        fpw.close()
        r = os.popen("rm /etc/nginx/conf.d/default.conf").readlines()
        r = os.popen("mv " + path_new_conf + " /etc/nginx/conf.d/default.conf").readlines()
        r = os.popen("/etc/init.d/nginx reload").readlines()  
        
    return request.data

if __name__ == '__main__':
    loadbalancer.run(host="0.0.0.0", port=8989)
