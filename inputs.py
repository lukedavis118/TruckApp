# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:14:57 2023

@author: luke_
"""
import datetime as dt

def inputParameters():
    inputs = {}
    ###################################################################
    #input variables
    username = 'contact@sweetwatertransportation.com'
    password = '#D@vis9063'
    
    # dt.datetime(year,month,day,hour, minute and second) in 24-hour clock
    inputs['date_start'] = dt.datetime(2023,8,29,6,0,0) # 6am
    inputs['date_end'] = dt.datetime(2023,8,30,18,0,0) # 6pm
     
    inputs['loadTime'] = 2.0 #hr
    inputs['unloadTime'] = 1.0 #hr
    inputs['avgSpeed'] = 56 #mph
    
    # Luke's house
    inputs['startCoords'] = [33.412402, -86.843263]
    inputs['startDayCity'] = 'Hoover, AL'
    inputs['endCoords'] = [33.412402, -86.843263]
    inputs['endDayCity'] = 'Hoover, AL'
    
    inputs['canDeliverNextDay'] = True
    inputs['startWithLoad'] = True
    inputs['startLoadCity'] = 'Eight Mile, AL'
      
    inputs['MPG_load'] = 6.5
    inputs['MPG_empty'] = 8.5
    inputs['diesel'] = 3.85 #input a value here, or type "np.nan" to get price from internet
    
    inputs['maintCostPerMile'] = 0.18
    return inputs, username, password