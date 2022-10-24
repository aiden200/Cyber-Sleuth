'''
Automation code to get traces on spotify.

Data is stored in the traces folder

To start venv, cd into comps directory and type source bin/activate
Required packages:
    Python 3.9
    selenium - automation of web browser interaction. Using chrome on this one
        Chrome driver version 106
    spotipy - allows us to use Spotify Web API
    scapy - take the wireshark traces: documentation https://scapy.readthedocs.io/en/latest/usage.html

For future ML:
    PyTorch
    Seaborn
    TSAI
'''
    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from scapy.all import *

import subprocess



def main():
    # chromedriver = "./chromedriver.exe"
    # options = Options()
    # options.binary_location = '/path/to/chrome'
    # driver = webdriver.Chrome(chromedriver, chrome_options=options)

    browser = webdriver.Chrome()
    # print("Opening browser")
    browser.get('https://google.com')
    # print("Opened!")
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #playing by clicking the play button
    capture = sniff(count=500)
    # print("sniffing")
    # t = AsyncSniffer()#iface="eth0", offline="file.pcap") # not sure 
    # t.start()
    # time.sleep(3)
    # results = t.stop()
    # print(results)
    # capture.summary()
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #pausing by clicking the play button
    i = 1
    wrpcap(f"traces/google/google_trace{i}.pcap", capture)
    browser.quit()
    try:
        with open(f'csv_files/google/google_trace{i}.csv','w') as f:
            subprocess.run(f"tshark -r traces/google/google_trace{i}.pcap -T fields\
            -e frame.number -e ip.src -e ip.dst \
            -E header=y -E separator=/t".split(), stdout =f)
    except Exception as e:
        print(f"Iteration: {i}\n error: {e}")
    #had to make link to tshark ln -s /Applications/Wireshark.app/Contents/MacOS/tshark /usr/local/bin/tshark
    # assert 'Yahoo' in browser.title

    # elem = browser.find_element(By.NAME, 'p')  # Find the search box
    # elem.send_keys('seleniumhq' + Keys.RETURN)





if __name__ == 'main':
    main()
main()
