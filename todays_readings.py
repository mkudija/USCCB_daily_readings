import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
import requests

import datetime as datetime
date = datetime.datetime.now().date()

datelist = pd.date_range(datetime.datetime.today(), periods=1).tolist()

def scrape_readings(currentDate):
    page = requests.get('http://www.usccb.org/bible/readings/{}.cfm'.format(currentDate.date().strftime('%m%d%y')))
    soup = BeautifulSoup(page.content, "html.parser")
    h3 = soup.find_all('h3')
    h4 = soup.find_all('h4')
    return h3, h4, soup

def print_readings(currentDate,
                   h4
                  ):
    
    # print date
    print('\n{}'.format(currentDate.date().strftime('%A %Y-%m-%d')))

    # print feast
    print(str(h3[2].contents[0]))
    
    # print readings
    for i in range(len(h4)):
        reading = str(h4[i].contents[0]).strip().replace('Or',' (or)').replace('Responsorial ','')
        verse = str(h4[i].contents[1].contents[0]).replace('\n','')
        if reading != 'Alleluia' and len(reading)>0:
            print('{0:10} {1}'.format(reading, verse))

for currentDate in datelist:
    h3, h4, soup = scrape_readings(currentDate)
    
    try:
        print_readings(currentDate,h4)
    except:
        print('\n{}: ERROR'.format(currentDate.date().strftime('%a %Y-%m-%d')))
    print('\n')


# run this automatically
## run: touch ~/.bash_profile; open ~/.bash_profile
## add: alias readings='cd Documents/GitHub/USCCB_daily_readings/; python todays_readings.py'