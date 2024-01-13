# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:23:59 2023

@author: Clive
"""

# import things here here

import scipy as sp
import numpy as np
import pandas as pd

# start running the other scripts

import Lists as lists
import Data_Frames as df
import Functions as func
import Optimisation as opt

import matplotlib.pyplot as plt

# start the cycle

def cycle(iterations) :
    
    
    i = 1
    while i <= iterations:  
        # production
        func.production_phase()
        
        # sell offers
        df.all_offers = func.sell_offer_market()
        
        # market accepts
        func.accept_sell_offer_market()
        
        # profit distribution
        func.profit_distribution()
        
        # calculate demand from utility function
        func.demand = opt.calculate_demand()
        
        # buy offers
        func.buy_offer_market()
        
        # market accepts
        func.accept_buy_offer_market()
        
        # households consume goods
        happiness = func.consume_goods()
        
        # prices adjust !!
        (df.prices, df.price_history, func.all_goods_price_history) = func.price_adjustment(i)
        
        # func.accelerate = func.price_acceleration(i)
        # no longer call this function here
   
        #increment the counter
        i += 1  

# show some data frames here

cycle(150)
      
goods = df.goods
prices = df.prices
production = df.production

all_offers = df.all_offers

price_history = df.price_history

demand = func.demand

# acceleration = func.accelerate
cycle_price_history = func.all_goods_price_history

#plot chart of price history that is generated


price_history.reset_index().pivot(index='cycle', columns='good', values='price').plot(marker='.')
