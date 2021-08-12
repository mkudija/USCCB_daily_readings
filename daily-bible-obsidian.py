#!/usr/bin/env python
# Python Version: 3.8.x

import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
import requests

import datetime as datetime
currentDate = datetime.datetime.today().date()


def scrape_readings(currentDate):
    page = requests.get('http://www.usccb.org/bible/readings/{}.cfm'.format(currentDate.strftime('%m%d%y')))
    soup = BeautifulSoup(page.content, "html.parser")
    h2 = soup.find_all('h2')
    h3 = soup.find_all('h3')
    add = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['address'])
    return h2, h3, add, soup


def print_readings(currentDate, h2, h3, add):
    
    # print date
    print('\n{}'.format(currentDate.strftime('%A %Y-%m-%d')))

    # print feast
    print(str(h2[3].contents[0]).replace('Ordinary Time','OT').replace('Saint','St.').replace('\n',''))
    
    # print readings
    for i in range(len(add)):
        reading = str(h3[i].contents[0]).strip().replace('Or',' (or)').replace('Responsorial ','')
        verse = str(add[i].contents[1].contents[0]).replace('\n','')
        if reading != 'Alleluia' and len(reading)>0:
            print('{0:10} {1}'.format(reading, verse))


def print_readings_obsidian(currentDate, h2, h3, add):
    
    # print feast
    print('\n**Daily Readings**')
    feast = str(h2[3].contents[0]).replace('Ordinary Time','OT').replace('Saint','St.').replace('\n','')
    print('*{}*'.format(feast.rstrip()))
    
    # print readings
    for i in range(len(add)):
        reading = str(h3[i].contents[0]).strip().replace('Or',' (or)').replace('Responsorial ','')
        verse = str(add[i].contents[1].contents[0]).replace('\n','')
        verseFront = verse.split(':')[0].replace(' ','-')
        try:
            if int(verseFront.split('-')[1]) < 10:
                verseFront = verseFront.split('-')[0] + '-0' + verseFront.split('-')[1]
        except:
            verseFront = 'Ps-'+verseFront
        verseBack = ', '.join(verse.split(':')[1:])
        verseLink = '[[{}]]:{}'.format(verseFront, verseBack)
        if reading != 'Alleluia' and len(reading)>0:
            print('{}: {}'.format(reading, verseLink))

def main():

    h2, h3, add, soup = scrape_readings(currentDate)
    
    # print_readings(currentDate, h2, h3, add)

    print_readings_obsidian(currentDate, h2, h3, add)

if __name__ == '__main__':
	main()