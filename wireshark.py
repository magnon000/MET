import os
import time
import random
import functools  # need pip install
import schedule  # need pip install
from selenium import webdriver  # need pip install

# http://chromedriver.storage.googleapis.com/index.html according to your chrome browser version
# install chromedriver_win32 to PATH : copy chromedriver.exe to C:\Users\???\AppData\Local\Programs\Python\Python310

# cmd_ws = '"C:\Program Files\Wireshark\Wireshark" -k -i 5'  # change the number after -i to your Ethernet interface
# os.system(cmd_ws)

# for now open wireshark manually and start capturing on Ethernet, ideally every hour every day from now on

list_web = ['https://www.sfr.fr/',
            'https://www.sfr.fr/offre-mobile/forfait-80go-4g-plus',
            'https://www.sfr.fr/tv-sfr',
            'https://tv.sfr.fr/browse/RefMenuItem::home']  # add more related websites

browser = webdriver.Chrome()
for web in list_web:
    browser.get(web)
    time.sleep(random.randint(1, 10))

# after all websites are shown, close wireshark and save as pcap file
