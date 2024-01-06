import time
from celery import shared_task

import urllib3
from bs4 import BeautifulSoup
import re

@shared_task
def really_long_wait():
    print("START SLEEP")
    time.sleep(5.0)
    print("STOP SLEEP")
    
# TODO: add async (?)
# TODO: add check in database (gather the data only once in a day - for data sync, and then store in database)
def gather_blood_type_stats():
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Vivaldi/6.4.3160.47'
    }
    url = r"https://www.rckik.poznan.pl"
    site = urllib3.request("GET", url, headers=headers)
    
    extracted = BeautifulSoup(site.data, "html.parser")
    
    drops = []
    for blood_type in extracted.find(id = "bloodsDetails").find_all("li"):
        blood_type_details = re.findall(r'(qVL|qL|qM|qF)">(.*?)<', str(blood_type))
        
        drops.append((blood_type_details[0][0], blood_type_details[0][1]))
        
    return drops