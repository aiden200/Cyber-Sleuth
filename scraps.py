'''
Scrap code file for CSI Comps
Developed by: Aiden Chang, Anders Shenholm
Last Updated: 1/11/2022 at 10:00 PM by Anders Shenholm
Please contact Aiden Chang for questions
'''

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scapy.all import *
from scapy.utils import RawPcapReader
from glob import glob
from get_traces import get_trace_ips, get_profile_ips
import chromedriver_autoinstaller
import random
import subprocess
import os
import csv
import datetime
import sys
import csv



'''
Function: get_noisy_trace_spotify
Sniffs 3000 packets after choosing and opening n websites from the list possible_websites. \
    A coin is flipped, if the result is 1, spotify will also be opened. Creates the csv and pcap file
    
Parameters:
    i - int, iteration(usually we are calling  this function multiple times)
    possible_websites - list of strings, the possible websites to open
        ex: possible_websites = ["https://google.com", "https://youtube.com","https://www.reddit.com/",\
         "https://www.carleton.edu/", "https://www.gmail.com", "https://www.github.com", \
            "https://www.discord.com","https://www.gradescope.com", "https://www.linkedin.com"]
    n - int, number of random websites to open
Returns:
    if spotify was NOT opened:
        csv file under: traces/noisy_traces/without_spotify/noisy_non_spotify[i].pcap
        pcap file under: csv_files/noisy_traces/without_spotify/noisy_non_spotify[i].csv
    if spotify was opened:
        csv file under: traces/noisy_traces/with_spotify/noisy_spotify[i].pcap
        pcap file under: csv_files/noisy_traces/with_spotify/noisy_spotify[i].csv
    function returns nothing
Example usage:
    get_noisy_trace_spotify(0, ["www.google.com","www.yahoo.com"], 1)
Notes:
    None
'''
def get_noisy_trace_spotify(i, possible_websites, n):
    if n > len(possible_websites):
        print("Error in function get_noisy_trace_spotify: random sample size larger than list possible_websites") 
        return
    browser = webdriver.Chrome()
    possible_websites = ["https://google.com", "https://youtube.com","https://www.reddit.com/",\
         "https://www.carleton.edu/", "https://www.gmail.com", "https://www.github.com", \
            "https://www.discord.com","https://www.gradescope.com", "https://www.linkedin.com"]
    open_website = random.choices(possible_websites, k=n)
    flip = random.randint(0, 1)
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

'''
Test function, used to experiment and comment some code that might be usefull in the future
'''
def test():
    # chromedriver = "./chromedriver.exe"
    # options = Options()
    # options.binary_location = '/path/to/chrome'
    # driver = webdriver.Chrome(chromedriver, chrome_options=options)
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #playing by clicking the play button
    # t = AsyncSniffer()#iface="eth0", offline="file.pcap") # not sure 
    # t.start()
    # time.sleep(3)
    # results = t.stop()
    # capture.summary()
    # driver.find_element_by_css_selector('button.Button-qlcn5g-0.kgFBvD').click() #pausing by clicking the play button
    # elem = browser.find_element(By.NAME, 'p')  # Find the search box
    # elem.send_keys('seleniumhq' + Keys.RETURN)
    
    #notes for second function
    # body = browser.find_element_by_tag_name("body")
    # search_box = browser.find_element("tag_name", "body")
    # search_box.send_keys('ChromeDriver')
    # search_box.submit()
    # Open a new window
    
    # Switch to the new window and open new URL
    '''
    offline analyzing
    pkts = sniff(offline='http_google.pcap')
    pkts.nsummary()s
    '''
    return None

# i used this to check a profile i generated vs a profile i generated from manual traffic
def compare_profiles(p1, p2):
    d1 = {}
    d2 = {}
    with open(f'ip_profiles/{p1}.csv',newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            d1[row[0]] = 0
    
    with open(f'ip_profiles/{p2}.csv',newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            d2[row[0]] = 0

    # ti = 0
    # for key in d1.keys():
    #     if key in d2:
    #         ti += 1
    # print (f'{ti/len(d1)*100:.0f}% of addresses in {p1} exist in {p2}')

    ti = 0
    for key in d2.keys():
        if key in d1:
            ti += 1
    print (f'{ti/len(d2)*100:.0f}% of addresses in {p2} exist in {p1}')
    return

# converts 32 bit ip profiles to 24 bit ip profiles
def generate_24_profile(p1):
    d1 = {}
    with open(f'ip_profiles/{p1}.csv',newline='') as f:
        reader = csv.reader(f)
        for row in reader:          #remove last piece of address
            ta = row[0].split(".")
            ts = ta[0] + "." + ta[1] + "." + ta[2]
            d1[ts] = 0
        
    with open(f'ip_profiles/{p1}_24.csv', 'w') as f:
        writer = csv.writer(f)
        for key in d1.keys():
            writer.writerow([key])


def analyze(filename):
    if not os.path.isfile(filename):
        print('"{}" does not exist'.format(filename), file=sys.stderr)
        sys.exit(-1)
    
    #Open pcap file and count packets
    count = 0
    for (pkt_data, pkt_metadata,) in RawPcapReader(filename):
        count += 1

    print('{} contains {} packets'.format(filename, count))


def main():
    pass

if __name__ == '__main__':
    main()