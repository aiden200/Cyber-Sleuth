'''
Helper function file for csv files.
Developed by: Aiden Chang
Last Updated: 10/30/2022 at 10:00 PM by Aiden Chang
Please contact Aiden Chang for questions
'''

import os
import sys
from scapy.utils import RawPcapReader
import csv

'''
Ignore
'''
def analyze(filename):
    if not os.path.isfile(filename):
        print('"{}" does not exist'.format(filename), file=sys.stderr)
        sys.exit(-1)
    
    #Open pcap file and count packets
    count = 0
    for (pkt_data, pkt_metadata,) in RawPcapReader(filename):
        count += 1

    print('{} contains {} packets'.format(filename, count))

'''
Reads a csv file and returns two dictionaries. 
source_ip - a dic with unique ip's of the source and the count of each ip
dest_ip - a dic with unique ip's of the destination and the count of each ip
'''
def getIps(filename):
    try:
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
    except Exception as e:
        print(f"Error in function getIps: {e}")


'''
Returns a list of unique ips
'''
def getIndividualIps(filename):
    return_list = []
    try:
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                if row[0] not in return_list:
                    return_list.append(row[0])
        return return_list
    except Exception as e:
        print(f"Error in function getIndividualIps: {e}")


'''
Testing purposes only
'''
def main():
    # filename = './traces/google/google_trace0.pcap'
    # analyze(filename)
    filename = "csv_files/google/google_trace1.csv"
    src_ip, dst_ip = getIps(filename)
    print(src_ip, dst_ip)

if __name__ == '__main__':
    main()