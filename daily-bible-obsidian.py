import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
import requests

import datetime as datetime
currentDate = datetime.datetime.today().date()
# currentDate = datetime.datetime.today().date() - datetime.timedelta(days = 2)


def scrape_readings(currentDate):
    page = requests.get('http://www.usccb.org/bible/readings/{}.cfm'.format(currentDate.strftime('%m%d%y')))
    soup = BeautifulSoup(page.content, 'html.parser')
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
        try:
            verse = str(add[i].contents[1].contents[0]).replace('\n','')
        except: # I think this is an issue when there are options for the Gospel? (i.e. on Feast of the Nativity of the Blessed Virgin Mary 2021-09-08)
            verse = ''
        # print(verse)

        # for numbered books, defined here: https://github.com/mkudija/BibleGateway-to-Obsidian-Catholic/blob/master/bg2obs.sh#L70    
        num_books = ['1 Sm ', '2 Sm ', '1 Kgs ', '2 Kgs ', '1 Chr ', '2 Chr ', '1 Mc ', '2 Mc ', '1 Cor ', '2 Cor ', 
                    '1 Thes ', '2 Thes ', '1 Tm ', '2 Tm ', '1 Pt ', '2 Pt ', '1 Jn ', '2 Jn ', '3 Jn ']
        if [x for x in num_books if(x in verse)]:
            verseFront = verse.split(':')[0]
            verseFront = verseFront.split(' ')[0]+' '+verseFront.split(' ')[1]+'-'+verseFront.split(' ')[2] # replace second space with '-'
            if int(verseFront.split('-')[1]) < 10:
                verseFront = verseFront.split('-')[0] + '-0' + verseFront.split('-')[1]
        else:
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