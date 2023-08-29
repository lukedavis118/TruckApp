# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 15:07:24 2023

@author: luke_
"""
import testTruckingFunctions as tf
import testTruckingCode as tfData
import datetime as dt
import pandas as pd
import numpy as np
import openrouteservice
import time
import sys
import requests
import inputs as ip

def getMarketPicture():    
    inputs, username, password = ip.inputParameters()
    ##########################################################################
    
    inputs2 = inputs.copy()
    
    # read in stored coordinates file
    coords = tf.getCoordinates() # loads in stored coordinates - Do Not Remove
    
    session = requests.Session()
    # login and get webdriver
    session = tf.truckstopLogin(session,username,password)
    
    
    savedToken = open('token.txt','r')
    token = savedToken.read()
    savedToken.close()
    try:
        (resultingTrips, data) = tfData.findTrips(inputs,session,coords,token)
    except:
        # login and get token
        print('Token has Expired. Getting new token...')
        token = tf.getToken(username,password)
        savedToken = open('token.txt','w')
        savedToken.write(token)
        savedToken.close()
        (resultingTrips, data) = tfData.findTrips(inputs,session,coords,token)
    
    
    
        
    def myFunc(e):
      return e['netRatePerHour']
    resultingTrips.sort(key=myFunc,reverse=True)
    resultingTrips2=resultingTrips.copy()
    
    print('\nFinding Trip Continuations')
    extendedTripsList = []
    avgNetRatePerHourList = []
    lengthOfResultingTrips = len(resultingTrips2)
    inputs2['date_start'] =inputs['date_start']+dt.timedelta(days=1)
    inputs2['date_end'] =inputs['date_end']+dt.timedelta(days=1)
    data = tf.getTruckstopLoads2(session,inputs2,token)
    
    cc = 0
    for row in resultingTrips2:
        cc += 1
        print('Processing {} out of {}'.format(cc,min(len(resultingTrips),lengthOfResultingTrips)))
        if row['nextDayDelivery'] is True:
            newStartLoadCity = row['itinerary'][-1]['destination']
            inputs2['startLoadCity'] = newStartLoadCity
            (avgNetRatePerHour, extendedTrips) = tfData.findTripsExtended(inputs2,session,coords,row,data)
            extendedTripsList.append(extendedTrips)
            avgNetRatePerHourList.append(avgNetRatePerHour)
        else:
            extendedTripsList.append(0)
            avgNetRatePerHourList.append(0)
        
    
    resultsDF = pd.DataFrame(resultingTrips2)
    resultsDF['marketPictureRPH'] = avgNetRatePerHourList
    resultsDF['rating'] = (resultsDF['marketPictureRPH'] + resultsDF['netRatePerHour'])/2
    resultsDF = resultsDF.sort_values(by=['rating'],ascending=False)
    resultsDF.reset_index(drop=True,inplace=True)
    
     
        
    netRate1 = round(resultsDF['netRate'])
    netRatePerHour1 = round(resultsDF['netRatePerHour'])
    totalRate1 = round(resultsDF['totalRate'])
    totalDistance1 = round(resultsDF['calcDistance'])
    marketPictureRPH = round(resultsDF['marketPictureRPH'])
    
    
    
    numberOfLoads=len(netRate1)
    original_stdout = sys.stdout # Save a reference to the original standard output
    
    # print itinerary for top 25 loads
    with open('results.txt', 'w') as f:
        
    
        sys.stdout = f # Change the standard output to the file we created.
    
        cc = 0
        while cc < numberOfLoads:
            cc += 1
            viewItinerary = tf.getTripItinerary(resultsDF,inputs,cc) # starts at 1
            print(' Net Rate:       $' ,netRate1[cc-1])
            print(' Total Rate:     $' ,totalRate1[cc-1])
            print(' Distance:        ' ,totalDistance1[cc-1], 'miles')
            print(' Net Rate/Hour:  $' ,netRatePerHour1[cc-1])
            print(' Market Grade:   $' ,marketPictureRPH[cc-1])
            print(' ***** Central Time Zones *****')
        
        sys.stdout = original_stdout # Reset the standard output to its original value
    
    print('\nFinished calculating!  Please view the "results" file for the full results.')
    
    # doYouWishToContinue = int(input('Enter "1" to extend trip or "0" to stop:'))
    # while doYouWishToContinue > 0:
    #     print('\nInput Trip Number to Get Extended Itinerary:')
    #     #client = openrouteservice.Client(key='5b3ce3597851110001cf62483a6cbc54da474d589da29850b9470abf')
    #     extendedTripItinerarySelector = int(input())-1
    #     extendedTripItinerary = extendedTripsList[extendedTripItinerarySelector]
    #     newStartLoadCity = extendedTripsList[extendedTripItinerarySelector][0]['itinerary'][0]['destination']
    #     inputs2['startLoadCity'] = newStartLoadCity
    #     resultingTrips = tf.getTripStatsFast2(extendedTripItinerary,inputs2)
    #     resultingTripsDF = pd.DataFrame(resultingTrips)
    #     resultingTripsDF = resultingTripsDF.sort_values(by=['netRatePerHour'],ascending=False)
    #     resultingTripsDF.reset_index(drop=True,inplace=True)
        
    #     netRate2 = round(resultingTripsDF['netRate'])
    #     netRatePerHour2 = round(resultingTripsDF['netRatePerHour'])
    #     totalRate2 = round(resultingTripsDF['totalRate'])
    #     totalDistance2 = round(resultingTripsDF['calcDistance'])
    
    #     numberOfLoads=len(netRate2)
         
    
        
    #     # print itinerary for top 25 loads
    #     cc = 0
    #     while cc < numberOfLoads:
    #         cc += 1
    #         viewItinerary = tf.getTripItinerary2(resultingTripsDF,inputs2,cc) # starts at 1
    #         print(' Net Rate:       $' ,netRate2[cc-1])
    #         print(' Total Rate:     $' ,totalRate2[cc-1])
    #         print(' Total Distance:  ' ,totalDistance2[cc-1], 'miles')
    #         print(' Net Rate/Hour:  $' ,netRatePerHour2[cc-1])
    #         print(' ***** Central Time Zones *****')
            
    #     doYouWishToContinue = int(input('Enter "1" to extend trip or "0" to stop:'))
    
    
        
    # print('\nThe program has concluded its calculations.')
    return resultsDF
    
