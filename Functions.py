# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 22:46:56 2023

@author: Clive
"""

# this is basic 2 good economy with agent interactions

import Lists as lists
import Data_Frames as df
import pandas as pd
import math

# define utility function

# utility_household = 2 * apple_consumed ^ 0.5 + 3 * banana_consumed ^ 0.5

# phase 1: production 

def production_phase():
    
    # need to generalise this
    
    # pandas.DataFrame.at --> selects value at specified row/column label 
    
    for good in lists.init_lists :
    
        df.goods.at["firms", good] = df.goods.at["firms", good] + df.production.at[0, good]
    
    print(df.goods)
    return df.goods

# phase 2: sell offer to market

def sell_offer_market():
    
    # creates the sell offers data frame
    # firms offer all goods produced to market at market price
    
    # sell offer data frame has good, supply, supply_accepted, and price as columns 
    
    # initialise list of sell offers
    
    offers = []
    
    # use pandas.DataFrame.at to select the value where "firms" is the row and column is "apples"
    # this uses index created at an earlier stage
    
    # iterate over each good in turn
    for good in lists.init_lists :

        good_offer = {
            "good" : good,
            "supply" : df.goods.at["firms", good],
            "supply_accepted" : 0,
            "price" : df.prices.at[good, "price"],
            "demand_accepted" : 0
        }
        
        offers.append(good_offer)
    
    all_offers = pd.DataFrame(offers)
    
    # create index for data frame - will be used later
    all_offers.set_index("good", inplace=True)
    
#sell_offer_market()
    print(all_offers)
    all_offers.index
    
    return all_offers
    
# phase 3: accept sell offers

def accept_sell_offer_market():
    
    # calculate total offer value and accept if market has enough money
    
    # returns product of rows (ie. price * supply) and sums them
    
    total_offer = (df.all_offers['supply'] * df.all_offers['price']).sum()

    print("Firm sell offer to market:", total_offer)
    
    # if market has enough then it accepts
    if total_offer <= df.goods.at["market", "money"] :
        # accepts full offer
        fraction_accept = 1
        
    # else market will partially accept the offer    
    else : 
        # accepts partial offer
     fraction_accept = df.goods.at["market", "money"] / total_offer
     
    # move money around according to fraction of offer accepted !
    
    # take goods from firms and give to market
    
    # iterate over each good in turn
    for good in lists.init_lists :
    
        df.all_offers.at[good, "supply_accepted"] = df.all_offers.at[good, "supply"] * fraction_accept      
        df.goods.at["firms", good] = df.goods.at["firms", good] - df.all_offers.at[good, "supply_accepted"]
        df.goods.at["market", good] = df.goods.at["market", good] + df.all_offers.at[good, "supply_accepted"]
    
    # exchange money

    df.goods.at["market", "money"] = df.goods.at["market", "money"] - total_offer * fraction_accept
    df.goods.at["firms", "money"] = df.goods.at["firms", "money"] + total_offer * fraction_accept
    
    print("df.goods at accept_sell_offer:", df.goods)
    
    return df.goods
        
#accept_sell_offer_market()

# phase 4: firms give money to households

def profit_distribution() :
    
    df.goods.at["households", "money"] = df.goods.at["households", "money"] + df.goods.at["firms", "money"]
    df.goods.at["firms", "money"] = 0
    
#profit_distribution()

# phase 5: buy offer to market    

def buy_offer_market():
    
    # once utility function has been optimised ... 
    
    # creates the buy offers data frame
    # households buy according to their money and utility function
        
    # adds new column onto the sell offers data frame
    
    # important that this is in the correct order !

    df.all_offers.insert(3, "demand", demand)
    
    # households will then use money to buy goods to maximise their utility function
    # need to find utility maximising amount first of all

    return df.all_offers
    
def accept_buy_offer_market():
    
    # market automatically accepts the buy offer as households already took into account constraints (could firms also do this?)

    print(df.all_offers.demand)
    total_offer = (df.all_offers.demand * df.all_offers.price).sum()
    print("Total_offer =", total_offer)

    # take goods from market and give to households
    
    # iterate over each good in turn
    for good in lists.init_lists :
    
        df.all_offers.at[good, "demand_accepted"] = df.all_offers.at[good, "demand"]
        df.goods.at["households", good] = df.goods.at["households", good] + df.all_offers.at[good, "demand_accepted"]
        df.goods.at["market", good] = df.goods.at["market", good] - df.all_offers.at[good, "demand_accepted"]
        
    # exchange money
    df.goods.at["market", "money"] = df.goods.at["market", "money"] + total_offer
    df.goods.at["households", "money"] = df.goods.at["households", "money"] - total_offer
    
    return df.goods

def consume_goods():
    
    # now the households eat all of their goods and gain happiness
        
    happiness = (2 *  df.goods.at["households", "apples"] ** 0.5 + 3 * df.goods.at["households", "bananas"] ** 0.5)
      
    df.goods.at["households", "apples"] = 0
    df.goods.at["households", "bananas"] = 0
    
    return happiness
    
def price_adjustment(cycle) :
    
    # create empty list to capture price history
    
    price_history = []
        
    # iterate over each good in turn
    for good in lists.init_lists :
                
        # apples and bananas are underpriced if market ends period with some goods in stock
        
        # run into floating point issues here - if value is close to 0 then go for it
        
        if math.isclose(df.goods.at["market", good], 0, abs_tol=0.01) :
            good_depleted = True
        else : 
            good_depleted = False
                
        # apples and bananas are overpriced if firms end period with some goods in stock
        
        if df.goods.at["firms", good] > 0.1 and df.all_offers.at[good, "supply"] > df.all_offers.at[good, "supply_accepted"] :
            good_remaining = True
        else : 
            good_remaining = False
                        
        # everything sold
        # if goods are selling then raise prices by arbitrary amount (price factor starts at 10%)
      
        if good_depleted == True and good_remaining == False :
            price_movement = "increase"
            #calculate price factor
            accelerate = price_acceleration(cycle, good, price_movement)
            #then adjust prices
            df.prices.at[good, "price"] = df.prices.at[good, "price"] * df.prices.at[good, "price_factor"]
            
            # record price movement
            good_price_history = {
                'cycle': cycle, 
                'good': good, 
                'price_movement': 'increase',
                'price': df.prices.at[good, "price"],
                'price_factor': df.prices.at[good, "price_factor"]
                }
            price_history.append(good_price_history)
                     
        # if firms sold less to market than last round (technically offered more than accepted, as don't keep track of supply_accepted)
        # if goods aren't selling then lower prices by arbitrary amount (price factor starts at 10%)
        
        elif good_depleted == True and good_remaining == True :
            price_movement = "decrease"
            #calculate price factor
            accelerate = price_acceleration(cycle, good, price_movement)
            #then adjust prices
            df.prices.at[good, "price"] = df.prices.at[good, "price"] / df.prices.at[good, "price_factor"]
           
            # record price movement
            good_price_history = {
                'cycle': cycle, 
                'good': good, 
                'price_movement': 'decrease',
                'price': df.prices.at[good, "price"],
                'price_factor': df.prices.at[good, "price_factor"]
                }
            price_history.append(good_price_history)
        
        # add this to a data frame
        # set index first
    all_goods_price_history = pd.DataFrame(price_history)
    all_goods_price_history.set_index(keys = ["cycle","good"], inplace = True)
    df.price_history = pd.concat([df.price_history, all_goods_price_history])
         
    return (df.prices, df.price_history, all_goods_price_history)

def price_acceleration(cycle, good, price_movement) :
    
    # if two periods of consecutive prive movement in the same direction are experienced then modify the price factors
    # alternatively, if prices are oscillating then slow movement of prices down    
    
    # for each unique good in list of goods ... 
    # lookup good in df.price_history for that good for current and last cycle ...
    # then compare and draw a price constant conclusion
    # adjust price factors in df.prices accordingly 
    
    # create empty list for return object - might not need this actually as we edit df.prices here (return df.prices?)
    
    accelerate = []
    
    # use list of goods to iterate over
   
    # for good in lists.init_lists :
        
    if cycle > 2 :
           
        # if price_movements match for at least three periods then accelerate (return a dictionary of the good plus info on acceleration status)
        
        if price_movement == 'increase' :
     
            if df.price_history.at[(cycle-1, good), 'price_movement'] == price_movement and df.price_history.at[(cycle-2, good), 'price_movement'] == price_movement:
                accelerate_good = {good : True}
                df.prices.at[good, "price_factor"] = min((df.prices.at[good, "price_factor"] * 1.1), 1.5)
                
            # stable price movement               
            elif df.price_history.at[(cycle-1, good), 'price_movement'] == price_movement :
                accelerate_good = {good : False}
                
            # else decelerate due to price oscillating
            else :
                accelerate_good = {good : False}
                # set to minimum of 1.2 for oscillating and then allow price_factor to slow at rate between 1 and 1.5, preferring value of price_factor
                df.prices.at[good, "price_factor"] = max(1.01, min((df.prices.at[good, "price_factor"] / 1.1), 1.5))     
            
        elif price_movement == 'decrease' :
        
            if df.price_history.at[(cycle-1, good), 'price_movement'] == price_movement and df.price_history.at[(cycle-2, good), 'price_movement'] == price_movement :
                accelerate_good = {good : True}
                df.prices.at[good, "price_factor"] = min((df.prices.at[good, "price_factor"] * 1.1), 1.5)
                
            # stable price movement               
            elif df.price_history.at[(cycle-1, good), 'price_movement'] == price_movement :
                accelerate_good = {good : False}
                
            # else decelerate due to price oscillating
            else : 
                accelerate_good = {good : False}
                # set to minimum of 1.2 for oscillating and then allow price_factor to slow at rate between 1 and 1.5, preferring value of price_factor
                df.prices.at[good, "price_factor"] = max(1.01, min((df.prices.at[good, "price_factor"] / 1.1), 1.5))
               
       # do not accelerate on 1st or 2nd cycles - stable price  
    else :
       accelerate_good = {good : False}
          
       # finally, append the acceleration status to the list
       accelerate.append(accelerate_good)
           
    return accelerate