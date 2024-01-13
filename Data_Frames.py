# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 13:08:27 2023

@author: Clive
"""

# sets up data frames for basic 2 good market

# import numpy as np
import pandas as pd

# create data frame with initial values of endowment of goods

# data frames work very differently in Python than datasets in SAS
# more efficient to create data frame as the last step from the individual rows
# rows can be stored in dictionaries
# and we can make a list of these dictionaries to make into the data frame

# have initialise_df function which creates the data frames in use elsewhere

def initialise_df() :

    #create empty list
    initial_endowment = []
    
    # Creating a new Python dictionary
    market_endowment = {
        "agent" : "market",
        "apples" : 0,
        "bananas" : 0,
        "money" : 1000
    }
    
    # create some more for the firms and households
    
    household_endowment = {
        "agent" : "households",
        "apples" : 0,
        "bananas" : 0,
        "money" : 0
    }
    
    firm_endowment = {
        "agent" : "firms",
        "apples" : 0,
        "bananas" : 0,
        "money" : 0
    }
    
    # Appending the list of dictionaries with the above dictionary
    # Using append() method
    initial_endowment.append(market_endowment)
    initial_endowment.append(household_endowment)
    initial_endowment.append(firm_endowment)
    
    # add this to a data frame
    
    goods = pd.DataFrame(initial_endowment)
    
    # create index for data frame - will be used later
    goods.set_index("agent", inplace=True)
    
    print(goods)
    goods.index
    
    # add initial prices to a data frame
    price_history = pd.DataFrame(columns = ['cycle', 'good', 'price_movement', 'price', 'price_factor'])
    price_history.set_index(keys = ["cycle","good"], inplace = True)
    
    initial_prices = {
        'good': ["apples", "bananas"], 
        'price': [3, 2],
        'price_factor': [1.1, 1.1]
    }
    prices = pd.DataFrame(initial_prices)
    
    # create index for data frame - will be used later
    prices.set_index("good", inplace=True)
    prices.index
    print(prices)
    
    # create a price history inside the data frame
    
    # add production to a data frame
    
    initial_production = {
        "apples": [100], 
        "bananas": [50]
    }
    production = pd.DataFrame(initial_production)
   
    
    return(goods, prices, price_history, production)

init_dfs = initialise_df()

#unpack the tuple that gets returned

(goods, prices, price_history, production) = init_dfs