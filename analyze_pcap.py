'''
File that takes offline pcacp files and alayzes
'''

import os
import sys
from scapy.utils import RawPcapReader
import csv

def analyze(filename):
    if not os.path.isfile(filename):
        print('"{}" does not exist'.format(filename), file=sys.stderr)
        sys.exit(-1)
    
    #Open pcap file and count packets
    count = 0
    for (pkt_data, pkt_metadata,) in RawPcapReader(filename):
        count += 1

    print('{} contains {} packets'.format(filename, count))

def getIps(filename):
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        next(spamreader)
        source_ip = {}
        dest_ip = {}
        for row in spamreader:
            if row[1] not in source_ip:
                source_ip[row[1]] = 1
            else:
                source_ip[row[1]] += 1
            if row[2] not in dest_ip:
                dest_ip[row[2]] = 1
            else:
                dest_ip[row[2]] += 1
        return source_ip, dest_ip


def main():
    # filename = './traces/google/google_trace0.pcap'
    # analyze(filename)
    filename = "csv_files/google/google_trace1.csv"
    src_ip, dst_ip = getIps(filename)
    print(src_ip, dst_ip)

if __name__ == '__main__':
    main()