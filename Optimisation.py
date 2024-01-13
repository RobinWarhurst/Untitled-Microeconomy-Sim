# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:40:32 2023

@author: Clive
"""

# this part uses spicy to solve some optimisation problems

# import scipy as sp
# import numpy as np

import Data_Frames as df
import inspect
# import Functions as func

# apples demand cannot exceed apples supply 
# bananas demand cannot exceed bananas supply
# budget constraint must hold

# budget constraint is : apple_price * apple_demand + banana_price * banana_demand <= household_money
# apple_demand <= market_supply
# banana_demand <= market_supply

from scipy.optimize import minimize

def inverse_utility_function(x) :
    apples_demand = x[0]
    bananas_demand = x[1]
    return  -(2 * apples_demand ** 0.5 + 3 * bananas_demand ** 0.5)

# def apples_supply_constraint(x) :
#     apples_demand = x[0]
#     return apples_demand - df.goods.at["market", "apples"]

# def bananas_supply_constraint(x) :
#     bananas_demand = x[1]
#     return bananas_demand - df.goods.at["market", "bananas"]

# this inequality constraint must be expressed in this form xp + yp <= money --> -1(xp + yp) >= -1(money)

def money_constraint(x) : 
    
    # assigns value of array x to apples_demand and bananas_demand
    # so it takes x as an array and assigns values within money constraint
    apples_demand = x[0]
    bananas_demand = x[1]
    # y = df.goods.at["households", "money"]
    return -(df.prices.at["apples", "price"] * apples_demand) -(df.prices.at["bananas", "price"] * bananas_demand) + df.goods.at["households", "money"]

def calculate_demand() :
    
    # this is a bound for each value of x
    bounds_apples_demand = (0, df.goods.at["market", "apples"])
    bounds_bananas_demand = (0, df.goods.at["market", "bananas"])

    bounds = [bounds_apples_demand, bounds_bananas_demand]

    constraint = {'type' : 'ineq', 'fun' : money_constraint}
    x0 = [1, 1]

    result = minimize(inverse_utility_function, x0, method = 'SLSQP', bounds=bounds, constraints=constraint)
    print(result.keys())
    print(result.message)
    print(result.success)
    print("df.goods at calculate_demand runtime:", df.goods)
    
    constraint_code = inspect.getsource(money_constraint)
    print("function:", constraint_code)
    
    return result.x
