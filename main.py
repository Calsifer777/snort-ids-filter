import sys
import os
import subprocess

def config_rule(src, dst):
    os.system(f'cp {src} {dst}')

def run_snort():
    os.system(f'snort -T -i ens33 -c /etc/snort/snort.conf')
    os.system(f'snort -A console -q -c /etc/snort/snort.conf -i ens33 &')

def stop_snort():
    os.system("ps -ef | grep snort | grep -v grep | awk '{print $2}' | xargs kill")
    
if __name__ == "__main__" :
    if len(sys.argv) < 8 and '-h' not in sys.argv:
    	print("try '-h' for more information")
    	sys.exit()
    else:
    	if '-h' in sys.argv:
    	    print('''
Usage: <src_rule_file> <target_rule_file> <test_option> <target_file> <payload_col> <src_port> <dst_ip> <dst_port>

target_rule_file : target_rule_file is a rule file that specifies include in snort.conf. The script modifies the target_rule_file each time to make the actual configured rule in snort.conf different, so that there is no need to modify the include of snort.conf every time

test_option to dst_port : can see the snort_test_script.py''')
    	else:
            #./20220101_00_ftp_cluster_mul_snort.rules.txt, /etc/snort/rules/test/target_rules.txt
            config_rule(sys.argv[1], sys.argv[2])
            run_snort()
            script_parm = " ".join(sys.argv[3:])
            # -p packet_table_20220101_00_中華電信_ftp_pcap.pickle tcp_payload 9999 192.168.0.19 80
            subprocess.call(f"python3 snort_test_script.py {script_parm}", shell=True)
            print('finish!')
            stop_snort()

