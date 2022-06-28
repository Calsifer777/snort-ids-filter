from scapy.all import *
import pandas as pd

def newest_log(log_dst):
    lists = os.listdir(log_dst)                                   #列出目錄的下所有文件和文件夾保存到lists
    lists.sort(key=lambda fn:os.path.getmtime(log_dst + "/" + fn))#按時間排序
    file_new = os.path.join(log_dst, lists[-1])
    return file_new

def get_payload(pkt):
    f_payload_list.append(pkt[TCP].payload)

def check_bytes(x):
    if type(x) == bytes:
        x = str(x)[2:-1]
    #else:
    #    x = str(bytes(x, 'utf-8'))[2:-1]
    return x

def packet_check_filter(x, f_payload_list):
    x = check_bytes(x)
    if x in f_payload_list:
        return False
    else:
        return True

def session_check_filter(x, f_payload_list):
    for i in x:
        i = check_bytes(i)
        if i in f_payload_list:
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 4 and '-h' not in sys.argv:
        print("try '-h' for more information")
        sys.exit()
    else:
        if '-h' in sys.argv:
            print(
            	'''
Usage: <log_dst_dir> <option> <input_file> <payload_col> <output_file>
log_dst_dir : dir that store snort log. (default is /var/log/snort/)
input_file : input Packet/Session table.
output_file : output filterd Packet/Session table.
            	'''
            )
        else:
            file_new = newest_log(sys.argv[1]) # /var/log/snort
            
            f_payload_list = []
            sniff(offline=file_new,prn=get_payload,store=0)
            f_payload_list = list(map(lambda x: bytes(x), f_payload_list))
            f_payload_list = list(map(lambda x: x.decode("utf-8"), f_payload_list))
            
            if sys.argv[2] == '-p':
                packet_table = pd.read_pickle(sys.argv[3])
                # packet_table['tmp_col'] = packet_table[sys.argv[4]].apply(check_bytes)
                packet_table = packet_table[packet_table[sys.argv[4]].apply(lambda x: packet_check_filter(x, f_payload_list))].reset_index()
                packet_table.to_pickle(sys.argv[5])
                
            elif sys.argv[2] == '-s':
                session_table = pd.read_pickle(sys.argv[3])
                session_table = session_table[session_table[sys.argv[4]].apply(lambda x: session_check_filter(x, f_payload_list))].reset_index()
                session_table.to_pickle(sys.argv[5])
        sys.exit()
