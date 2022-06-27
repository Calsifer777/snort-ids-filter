import pickle
import pandas as pd
from scapy.all import *
from tqdm import tqdm
import time

def check_bytes(x):
    if type(x) == bytes:
        x = str(x)[2:-1]
    # else:
    #     x = str(bytes(x, 'utf-8'))[2:-1]
    return x

######## Cluster Packet Test ########
# def Cluster_test():
#     #data = pd.read_pickle("../testcase/sessiontable_clustered_20210503_1.pkl")
#     data = pd.read_pickle(target_file)
#     regex_result=[]
#     for i in data["sess_cluster"]:
#         regex_result.append(i)
#     data['regex'] = regex_result
#     cluster_max  = data["sess_cluster"].max(0)
#     testcase={}
#     for c in range(cluster_max+1):
#         fliter = (data["sess_cluster"] == c)
#         tmp = []
#         for i in data[fliter]["preprocessed_payload"]:
#         # for i in data[fliter]["raw_payload"]:
#             tmp.append(i[0])
#         # tmp = list(set(tmp))
#         testcase[c] = tmp
    
#     cnt = 0
#     for k, v in tqdm(testcase.items()):
#         for j in tqdm(v): #sess_cluster
#             pack=IP(dst='192.168.1.116')/TCP(sport=9999, dport=80)/j #測試目標 IP, srcport
#             # print(pack)
#             send(pack)
#             cnt += 1
#         print(f"Cluster {k} total packet: {cnt}")

########## Session Test ##########
def session_test():
    #data = pd.read_pickle('./clustered_20220101_00_中華電信_http.pkl')
    target_file, payload_col, src_port, dst_ip, dst_port = parm
    data = pd.read_pickle(target_file)
    cnt = 0
    
    payload_list = []
    for i in tqdm(data['tcp_i_payload_list']):
        payload_list += check_bytes(i)
    
    for i in tqdm(list(set(payload_list))):
        print(i)
        pack=IP(dst=dst_ip)/TCP(sport=int(src_port), dport=int(dst_port))/i #測試目標 IP, srcport
        send(pack)
        cnt += 1
    print(f"total packet: {cnt}")
########### Packet Test ############
def packet_test(parm):
    # data = pd.read_pickle('./packet_table_20220101_00_中華電信_clusterid.pickle')
    target_file, payload_col, src_port, dst_ip, dst_port = parm
    data = pd.read_pickle(target_file)
    cnt = 0   
    
    #'tcp_payload', 192.168.0.19 9999, 80
    payload = data[payload_col].apply(check_bytes)
    for i in list(set(payload)):
        print(i)
        pack=IP(dst=dst_ip)/TCP(sport=int(src_port), dport=int(dst_port))/i #測試目標 IP, srcport
        send(pack)
        cnt += 1
    print(f"total packet: {cnt}")
    
if __name__ == '__main__':
    if len(sys.argv) < 6 and sys.argv[1] != '-h':
    	print("try '-h' for more information")
    	sys.exit()
    else:
        if sys.argv[1] == '-s':
            session_test(sys.argv[2:7])
        elif sys.argv[1] == '-p':
            packet_test(sys.argv[2:7])
        # elif sys.argv[1] == '-c':
        #     Cluster_test(sys.argv[2:7])
        elif sys.argv[1] == '-h':
            print(
            	'''
Usage: <option> <target_file> <payload_col> <src_port> <dst_ip> <dst_port>
-s : session mode filter test.
-p : packet mode filter test.
            	'''
            )
        else:
            print("try '-h' for more information")
            sys.exit()
            
    

