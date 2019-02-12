# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:14:46 2018

Schedule hourly input of verified IESO demand values and input into postgres database
"""

## Add module path to sys.path
from modules import dataschedule #module for adding to postgres database

## Database login info
database = ''
password = ''
host = ''

## Create dataschedule object with database, password and host loc
obj = dataschedule.dataschedule(database, password, host)
obj.sched_interval(interval='hourly', job = obj.iesoactual)
obj.sched_interval(interval='at', job = obj.iesoforecast, sched_time="10:00")
obj.sched_interval(interval='at', job = obj.myforecast, sched_time="10:00")
obj.sched_interval(interval='at', job = obj.myforecast, sched_time="22:00")
obj.sched_interval(interval='at', job = obj.myforecast1, sched_time="10:00")
obj.sched_interval(interval='at', job = obj.myforecast1, sched_time="22:00")

## Initialize scheduling
obj.sched_init()

    
