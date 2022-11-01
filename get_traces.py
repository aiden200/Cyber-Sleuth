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

Developed by: Aiden Chang
Last Updated: 10/30/2022 at 10:00 PM by Aiden Chang
Please contact Aiden Chang for questions
'''

'''
TODO:
    protocals

Open google, take the ip address, which will include background processes, build a csv file. start building profile on spotify traces.
Filter out Carleton ip addresses and arp
Include frequencies

Experiment ip addresses
take just background
compare between different members
compare between different os's 
comment out better and update
check if selnium can open apps

build background profile
chrome profile = chrome traces - background profile
spotify profile = spotify traces - chrome profile - background profile

Experiments
Chrome profile
Chrome while searching profile

Chrome profile - Chrome while searching profile > 1

Compare ips in different location
ips on web browser vs app?
ips on app logged out vs logged in




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
import chromedriver_autoinstaller

def install_chromdriver():
    #Installs chromedriver
    print("Installing chromedriver")
    try:
        chromedriver_autoinstaller.install()
        return 0
    except Exception as e:
        print(f"Failed to download chromdriver with exception: {e}")
        return -1



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


'''
Function: sniff_website
Sniffs count packets on a website and creates the csv file and the pcap file.

Parameters:
    i - int, iteration(usually we are calling  this function multiple times)
    website - str, the website we are sniffing (ex: "www.google.com")
    name - str, the name we are using for the file (ex: "google")
    count - int, number of packets sniffing, default to 1000
Returns:
    csv file under: csv_files/[name]/[name_trace][i].csv
    pcap file under: traces/[name]/[name_trace][i].pcap
    function returns nothing
Example usage:
    sniff_website(0, "www.google.com", "google")
Notes:
    for the subprocess.open tshark command to work, you might need to link tshark 
    mine was done like this:
        tshark ln -s /Applications/Wireshark.app/Contents/MacOS/tshark /usr/local/bin/tshark
'''
def sniff_website(i, website, name, count = 1000):
    
    browser = webdriver.Chrome()
    if website != 0:
        browser.get(website)
    MYDIR = (f"traces/{name}")
    CHECK_FOLDER = os.path.isdir(MYDIR)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        print(f"Folder {name} does not exist. Creating new....")
        os.makedirs(MYDIR)
        os.makedirs(f"csv_files/{name}")
    capture = sniff(count=1000)
    wrpcap(f"traces/{name}/{name}_trace{i}.pcap", capture)
    browser.quit()
    try:
        with open(f'csv_files/{name}/{name}_trace{i}.csv','w') as f:
            subprocess.run(f"tshark -r traces/{name}/{name}_trace{i}.pcap -T fields\
            -e frame.number -e ip.src -e ip.dst \
            -E header=y -E separator=/t".split(), stdout =f)
    except Exception as e:
        print(f"Iteration: {i}\n error: {e}")




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


'''
Function: build_ip_profiles
Builds a csv file with all the possible unique ip address that the website represents
    
Parameters:
    website - str, the website we are profiling. This must be identical to the folder scanning. (ex: "google")
Returns:
    profile built in /ip_profiles/{website}.csv
    function returns nothing
Example usage:
    build_ip_profiles("google")
Notes:
    If the folder does not exist in csv files it will throw and error.
'''
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
        # print(new_ips)
        with open(write_path, write_type) as csv_writer:
            writer_object = csv.writer(csv_writer)
            for ip in new_ips:
                writer_object.writerow([ip])




'''
Builds a profile of background apps.
Sniffs 500 packets and closes

Notes:
Consider building off of stopping after time
'''
def build_background_trace_profile():
    start = time.time()
    end = time.time()
    time_consumed=end-start
    for i in range(100):
        MYDIR = (f"traces/background")
        CHECK_FOLDER = os.path.isdir(MYDIR)
        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            print(f"Folder background does not exist. Creating new....")
            os.makedirs(MYDIR)
            os.makedirs(f"csv_files/background")
        capture = sniff(count=500)
        wrpcap(f"traces/background/background_trace{i}.pcap", capture)
        try:
            with open(f'csv_files/background/background_trace{i}.csv','w') as f:
                subprocess.run(f"tshark -r traces/background/background_trace{i}.pcap -T fields\
                -e frame.number -e ip.src -e ip.dst \
                -E header=y -E separator=/t".split(), stdout =f)
        except Exception as e:
            print(f"Iteration: {i}\n error: {e}")
    
    build_ip_profiles("background")


'''
Filters out the ips. subtracts ips that exist in filter_website and target_website. \
    returns ips left from target_website
'''
def filter_ips(target_website, filter_website):
    if not (os.path.exists(f"ip_profiles/{target_website}") and os.path.exists(f"ip_profiles/{filter_website}")):
        if not os.path.exists(f"ip_profiles/{target_website}"):
            print(f"Error in function filter_ips: File does not exist: ip_profiles/{target_website}")
        if not os.path.exists(f"ip_profiles/{filter_website}"):
            print(f"Error in function filter_ips: File does not exist: ip_profiles/{filter_website}")
        return -1
    
    target_ips = getIndividualIps(f"ip_profiles/{target_website}")
    filter_ips = getIndividualIps(f"ip_profiles/{filter_website}")

    filtered_list = []
    for ip in target_ips:
        if ip not in filter_ips:
            filtered_list.append(ip)
    
    with open(f"ip_profiles/{target_website}", "w") as csv_writer:
        writer_object = csv.writer(csv_writer)
        for ip in filtered_list:
            writer_object.writerow([ip])
    return 0





##################################################################################################
# After this section its the usage of the above functions.
##################################################################################################

def build_chrome_profile():
    build_background_trace_profile()
    for i in range(100):
        sniff_website(i, 0, "chrome")
    build_ip_profiles("chrome")
    if filter_ips("chrome", "background") != 0:
        print("Failed in making chrome profile")



#TODO: def build_profile_without_noise(website, name):


'''
Usages of the functions above.
'''
def main():
    install_chromdriver() # MUST CALL
    possible_websites = ["https://google.com", "https://youtube.com","https://www.reddit.com/",\
         "https://www.carleton.edu/", "https://www.gmail.com", "https://www.github.com", \
            "https://www.discord.com","https://www.gradescope.com", "https://www.linkedin.com"]
    n = 3
    for i in range(100):
        # sniff_website(i, "www.google.com", "google")
        # get_noisy_trace_spotify(i, possible_websites, n)
        pass
    # build_ip_profiles("google")
    sniff_website(1, "www.google.com", "google")
main()

    
