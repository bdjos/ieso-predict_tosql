# -*- coding: utf-8 -*-

"""

Schedule hourly input of verified IESO demand values and input into postgres database
"""

## Add module path to sys.path

from sqlmodules import dataschedule #module for adding to postgres database

## Database login info
database = 'bjos'
password = '3iRM7Ihr@'
host = '138.197.155.217'

## Create dataschedule object with database, password and host loc. Schedule input and init.
obj = dataschedule.dataschedule(database, password, host)
obj.sched_interval(interval='at', job = obj.iesoforecast)
obj.sched_init()
