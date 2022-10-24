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




def main():
    # chromedriver = "./chromedriver.exe"
    # options = Options()
    # options.binary_location = '/path/to/chrome'
    # driver = webdriver.Chrome(chromedriver, chrome_options=options)

    browser = webdriver.Chrome()
    print("Opening browser")
    browser.get('https://open.spotify.com/collection/tracks')
    print("Opened!")
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #playing by clicking the play button
    print("sniffing")
    t = AsyncSniffer()#iface="eth0", offline="file.pcap") # not sure 
    t.start()
    time.sleep(3)
    results = t.stop()
    print(results)
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #pausing by clicking the play button


    # assert 'Yahoo' in browser.title

    # elem = browser.find_element(By.NAME, 'p')  # Find the search box
    # elem.send_keys('seleniumhq' + Keys.RETURN)

    browser.quit()




if __name__ == 'main':
    main()
main()
