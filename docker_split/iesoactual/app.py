# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:14:46 2018

Step 1:
    Downloads all necessary data for graphing IESO peak predictions. 
    1. Download weather data from accuweather API and run a prediction using fastai prediction model
    2. Download IESO prediction data (XML format?)
    3. Download IESO verified data

Step 2:
    Stores all data in SQL database

In/out of SQL database using pandas to_db and from_db

@author: BJoseph
"""

import pandasdb
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
import xml.etree.ElementTree as ET #module for parsing XML files
import requests #module for wget of xml file
import os 
import pandas as pd
import schedule
import time

class sched_input():
    def __init__(self, database, password, host):
        self.database = database
        self.password = password
        self.host = host
    
    def xml_parse(self, url, xml_direct, xml_file):
        'Parse .xml files and return root object'
        response = requests.get(url)
        xml_loc = os.path.join(xml_direct, xml_file)
        with open(xml_loc, 'wb') as f:
            f.write(response.content)
        
        tree = ET.parse(xml_loc)
        root = tree.getroot()
        return root

    def iesoactual(self):
        ##get .xml file from ieso website
        date_dt = datetime.datetime.now() + datetime.timedelta(hours=-1)
        
        ## Check if hour is 00 then convert to IESO format
        if date_dt.hour == 0: 
            date_dt = date_dt + datetime.timedelta(hours=-1)
            date_str = datetime.datetime.strftime(date_dt, "%Y%m%d")
            date_str = date_str + '24'
        else:
            date_str = datetime.datetime.strftime(date_dt, "%Y%m%d%H")
        
        url = f'http://reports.ieso.ca/public/RealtimeConstTotals/PUB_RealtimeConstTotals_{date_str}.xml'
        xml_direct = 'data'
        xml_file = 'iesoactual.xml'         
    
        root = self.xml_parse(url, xml_direct, xml_file) ##Parse xml file
        
        ##
        demand = []
        for i in range(12):
            demand.append(float(root[1][2][i][8][1].text))  
        total_demand = [sum(demand)/len(demand)]
        
        timeless_dt = [datetime.datetime(year=date_dt.year, month=date_dt.month, day=date_dt.day, hour=date_dt.hour)]
        df = pd.DataFrame({'Date/Time': timeless_dt, 'IESO Actual Demand': total_demand})
        
        #To Database
        table = 'IESOACTUAL'
        dtypes = [DateTime(), Float()]
        db = pandasdb.pandasdb(self.database, self.password, self.host, table)
        db.pd_to_db(dtypes, df, if_exists='append')
        
        print(f'IESO Actual Data successfully added to database at {datetime.datetime.strftime(datetime.datetime.now(), "%H:%M")}')
            
    def sched_interval(self, interval, job, sched_time = '00:00'):
        '''
        interval == 'hourly' or 'at or 'minute''
        sched_time default '00:00'
        '''
        if interval not in ('hourly', 'at', 'minute'):
            print('Please enter either \'hourly\' or \'at\' for the interval')
        elif interval == 'minute':
            schedule.every(1).minutes.do(job)
        elif interval == 'hourly':
            schedule.every().hour.do(job)
        elif interval == 'at':
            schedule.every().day.at(sched_time).do(job)
        
        while 1:
            schedule.run_pending()
            time.sleep(1)      
            
if __name__ == "__main__":
    database = 'bjos'
    password = '3iRM7Ihr@'
    host = '138.197.155.217'
    
    obj = sched_input(database, password, host)
    obj.sched_interval(interval='hourly', job = obj.iesoactual)


    