from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scapy.all import *
import random
import subprocess
import os
from glob import glob
import csv
from analyze_pcap import getIps, getIndividualIps
import chromedriver_autoinstaller
import datetime

# installs chromedriver
def install_chromedriver():
    print("Installing chromedriver")
    try:
        chromedriver_autoinstaller.install()
        return 0
    except Exception as e:
        print(f"Failed to download chromdriver with exception: {e}")
        return -1

# for num_traces, use google.com in Chrome to search some random 2 letter string 
# capture begins with the search and ends after 1000 packets are captured.
# outputs full pcap files and csv files that just include IP addresses
def sniff_google_search(num_traces):
    #make folders for results
    folder_id = "google_search_" + datetime.datetime.now().strftime("%m-%d-%y_%H.%M.%S")
    os.makedirs(f"traces/{folder_id}")
    os.makedirs(f"csv_files/{folder_id}")

    #generate query, make search, take capture
    for i in range(1, num_traces + 1):
        query = chr(random.randrange(97, 123)) + chr(random.randrange(97, 123))
        browser = webdriver.Chrome()
        browser.get("https://google.com")
        inputs = browser.find_elements(By.TAG_NAME, "input")
        for j in range(len(inputs)):
            if inputs[j].value_of_css_property("display") == "flex":
                search_index = j
        inputs[search_index].send_keys(query)
        inputs[search_index].send_keys(Keys.RETURN)
        capture = sniff(count=1000)
        browser.quit()
        
        #record capture results
        wrpcap(f"traces/{folder_id}/trace{i}.pcap", capture)
        try:
            with open(f'csv_files/{folder_id}/trace{i}.csv','w') as f:
                subprocess.run(f"tshark -r traces/{folder_id}/trace{i}.pcap \
                -T fields -e frame.number -e ip.src -e ip.dst \
                -E header=y -E separator=/t".split(), stdout =f)
        except Exception as e:
            print(f"Iteration: {i}\n error: {e}")

    

# logs in to spotify web player, then searches and plays a (somewhat) random song. 
# capture begins with clicking play on the song and ends after 5000 packets are captured
# outputs full pcap files and csv files that just include IP addresses
def sniff_spotify_song_play(num_traces):
    #make folders for results
    folder_id = "random_spotify_song_" + datetime.datetime.now().strftime("%m-%d-%y_%H.%M.%S")
    os.makedirs(f"traces/{folder_id}")
    os.makedirs(f"csv_files/{folder_id}")

    #read in account credentials
    config = open('config.txt', 'r')    
    username = config.readline()
    password = config.readline()
    config.close()

    for i in range(1, num_traces + 1):
        #generate query, navigate spotify, take capture 
        query = chr(random.randrange(97, 123)) + chr(random.randrange(97, 123))
        browser = webdriver.Chrome()
        browser.get("https://accounts.spotify.com/")    #go to login screen 
        username_input = browser.find_element(By.ID, "login-username")
        password_input = browser.find_element(By.ID, "login-password")
        login_button = browser.find_element(By.ID, "login-button")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        webplayer_button = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='web-player-link']")))
        webplayer_button.click()    #go to web player
        search_menu = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[href='/search']")))
        search_menu.click()         #go to search tab
        search_bar = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='search-input']")))
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
        song_results = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[width='40']")))
        song_results.click()
        capture = sniff(count=5000)
        browser.quit()

        #record capture results
        wrpcap(f"traces/{folder_id}/trace{i}.pcap", capture)
        try:
            with open(f'csv_files/{folder_id}/trace{i}.csv','w') as f:
                subprocess.run(f"tshark -r traces/{folder_id}/trace{i}.pcap \
                -T fields -e frame.number -e ip.src -e ip.dst \
                -E header=y -E separator=/t".split(), stdout =f)
        except Exception as e:
            print(f"Iteration: {i}\n error: {e}")

# takes name of a dir in traces and converts all pcap files into csv files with in and out ip addresses
# used currently to convert manual traces into pcap files
def pcap_to_csv(trace_name):
    MYDIR = (f"csv_files/{trace_name}")
    CHECK_FOLDER = os.path.isdir(MYDIR)
    if not CHECK_FOLDER:
        print(f"Folder 'csv_files/{trace_name}' does not exist. Creating new....")
        os.makedirs(MYDIR)

    root_dir = str(os.path.dirname(os.path.abspath(__file__)))
    full_dir = root_dir + "/traces/" + trace_name
    for filename in os.listdir(full_dir):
        try:
            with open(f'csv_files/{trace_name}/{filename}.csv','w') as f:
                subprocess.run(f"tshark -r traces/{trace_name}/{filename} \
                -T fields -e frame.number -e ip.src -e ip.dst \
                -E header=y -E separator=/t".split(), stdout =f)
        except Exception as e:
            print(f"Iteration: {filename}\n error: {e}")

