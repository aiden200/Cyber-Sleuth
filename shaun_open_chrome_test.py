from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


def main():
    install_chromdriver()
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com")

main()
