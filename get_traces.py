'''
Automation code to get traces on spotify.

Data is stored in the traces folder

To start venv, cd into comps directory and type source bin/activate
Required packages:
    Python 3.9
    selenium - automation of web browser interaction. Using chrome on this one
        Chrome driver version 106
    scapy - take the wireshark traces: documentation https://scapy.readthedocs.io/en/latest/usage.html

For future ML:
    PyTorch
    Seaborn
    TSAI
'''
'''
TODO:
    protocals

Open google, take the ip address, which will include background processes, build a csv file. start building profile on spotify traces.


'''
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from scapy.all import *
import random
import subprocess
import os
from glob import glob
import csv
from analyze_pcap import getIps, getIndividualIps



def main(i):
    # chromedriver = "./chromedriver.exe"
    # options = Options()
    # options.binary_location = '/path/to/chrome'
    # driver = webdriver.Chrome(chromedriver, chrome_options=options)

    browser = webdriver.Chrome()
    # print("Opening browser")
    browser.get('https://google.com')
    # print("Opened!")
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #playing by clicking the play button
    capture = sniff(count=1000)
    # print("sniffing")
    # t = AsyncSniffer()#iface="eth0", offline="file.pcap") # not sure 
    # t.start()
    # time.sleep(3)
    # results = t.stop()
    # print(results)
    # capture.summary()
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #pausing by clicking the play button
    wrpcap(f"traces/google/google_trace{i}.pcap", capture)
    browser.quit()
    try:
        with open(f'csv_files/google/google_trace{i}.csv','w') as f:
            subprocess.run(f"tshark -r traces/google/google_trace{i}.pcap -T fields\
            -e frame.number -e ip.src -e ip.dst \
            -E header=y -E separator=/t".split(), stdout =f)
    #protocals
    except Exception as e:
        print(f"Iteration: {i}\n error: {e}")
    #had to make link to tshark ln -s /Applications/Wireshark.app/Contents/MacOS/tshark /usr/local/bin/tshark
    # assert 'Yahoo' in browser.title

    # elem = browser.find_element(By.NAME, 'p')  # Find the search box
    # elem.send_keys('seleniumhq' + Keys.RETURN)

    '''
    offline analyzing
    pkts = sniff(offline='http_google.pcap')
    pkts.nsummary()s
    '''

def get_random_trace(i):
    browser = webdriver.Chrome()
    possible_websites = ["https://google.com", "https://youtube.com","https://www.reddit.com/",\
         "https://www.carleton.edu/", "https://www.gmail.com", "https://www.github.com", \
            "https://www.discord.com","https://www.gradescope.com", "https://www.linkedin.com"]
    open_website = random.choices(possible_websites, k=3)
    flip = random.randint(0, 1)
    # body = browser.find_element_by_tag_name("body")
    # search_box = browser.find_element("tag_name", "body")
    # search_box.send_keys('ChromeDriver')
    # search_box.submit()
    # Open a new window
    
    # Switch to the new window and open new URL
    j = 0

    if flip:
        browser.get('https://spotify.com')
        browser.execute_script("window.open('');")
        j+=1
        browser.switch_to.window(browser.window_handles[j])

    for websites in open_website:
        browser.get(websites)
        browser.execute_script("window.open('');")
        j +=1
        browser.switch_to.window(browser.window_handles[j])
    capture = sniff(count=3000)

    
    name = f"traces/noisy_traces/without_spotify/noisy_non_spotify{i}.pcap"
    csv_name = f"csv_files/noisy_traces/without_spotify/noisy_non_spotify{i}.csv"
    if flip:
        name = f"traces/noisy_traces/with_spotify/noisy_spotify{i}.pcap"
        csv_name = f"csv_files/noisy_traces/with_spotify/noisy_spotify{i}.csv"
    wrpcap(name, capture)
    try:
        with open(csv_name,'w') as f:
            subprocess.run(f"tshark -r {name} -T fields\
            -e frame.number -e ip.src -e ip.dst \
            -E header=y -E separator=/t".split(), stdout =f)
    except Exception as e:
        print(f"Iteration: {i}\n error: {e}")
    browser.quit()


def build_ip_profiles(website):
    # curr_path = os.path.dirname(os.path.abspath(__file__))
    csv_profile_list = glob("csv_files/*")
    folder = ""
    for name in csv_profile_list:
        if website in name:
            folder = name
            break
    if not folder:
        print(f"Error in build ip profile: no csv file built for website {website}")
    else:
        ip_sets = []
        new_ips = []
        write_type = "w"
        write_path = f"./ip_profiles/{website}.csv"
        if os.path.exists(write_path):
            write_type = "a"
            ip_sets = getIndividualIps(write_path)

        csv_files = glob(f"{folder}/*")
        for file in csv_files:
            src_ip, dst_ip = getIps(file)

            for key in src_ip:
                if key and key not in ip_sets:
                    new_ips.append(key)
                    ip_sets.append(key)
            for key2 in dst_ip:
                if key2 and key2 not in ip_sets:
                    new_ips.append(key2)
                    ip_sets.append(key2)
        print(new_ips)
        with open(write_path, write_type) as csv_writer:
            writer_object = csv.writer(csv_writer)
            for ip in new_ips:
                writer_object.writerow([ip])



        



# if __name__ == 'main':
#     main()

# for i in range(10):
#     get_random_trace(i)
build_ip_profiles("google")
    
