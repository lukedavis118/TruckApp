# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 20:19:52 2023

@author: luke_
"""

import streamlit as st
import pandas as pd
import numpy as np
import marketPicture as mp
import datetime as dt

st.title('Working Trucking Code')


resultsDF = mp.getMarketPicture()
    
f = open("results.txt", "r")
for x in f:
  st.write(x)