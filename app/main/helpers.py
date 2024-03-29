from datetime import datetime, timedelta
import urllib3
from bs4 import BeautifulSoup
import re
import unicodedata

from ..models import BloodState, Post
from .. import db

# TODO: add check in database (gather the data only once in a day - for data sync, and then store in database)
def gather_blood_type_stats():
    
    # check if blood_state is up-to-date in database and return data from it
    my_data = BloodState.query.all()
    
    if my_data[0].last_update + timedelta(hours=3) < datetime.now():
        # otherwise - get data from the website
        print("DEBUG: visit website and gather newest blood stats!")
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
            
        for blood_data in my_data:
            for blood in drops:
                if blood_data.blood_type == blood[1]:
                    blood_data.amount = blood[0]
            blood_data.last_update = datetime.now()
        
        db.session.commit()
        
        # TODO: add order assertion - for the blood type to be always at the correct position
        return drops
        
    print("DEBUG: blood stats gathered from database.")
    
    drops = []
    for blood_data in sorted(my_data, key=lambda BloodState: BloodState.id):
        drops.append((blood_data.amount, blood_data.blood_type))
    
    return drops

def process_title(title):
    '''
    Helper method handling processing the title for news subsite:
    * lowercase whole text
    * replace characters with HTML escape alternatives
    * replace whitespace with dashes
    * etc.
    '''
    title_normalized = title.lower()
    title_normalized = re.sub(r'(\s|\_|=)', '-', title_normalized)
    title_normalized = ''.join(c for c in unicodedata.normalize('NFD', title_normalized)
                   if unicodedata.category(c) != 'Mn')
    title_normalized = re.sub(r'[^a-zA-Z0-9\-]', '', title_normalized)
    return title_normalized

def get_all_posts():
    return Post.query.all()