# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:14:46 2018

Schedule hourly input of verified IESO demand values and input into postgres database
"""

from sqlmodules import dataschedule #module for adding to postgres database

## Database login info
database = 'bjos'
password = '3iRM7Ihr@'
host = '138.197.155.217'

## Create dataschedule object with database, password and host loc. Schedule input and init.
obj = dataschedule.dataschedule(database, password, host)

## Schedule SQL input at 10:00am & pm
obj.sched_interval(interval='at', job = obj.iesoactual, sched_time='10:00')
obj.sched_interval(interval='at', job = obj.iesoactual, sched_time='22:00')

## Initiate Scheduling
obj.sched_init()

    
