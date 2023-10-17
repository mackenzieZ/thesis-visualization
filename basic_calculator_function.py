import nashpy as nash
import numpy as np
import ast
from sympy import symbols, Eq, solve

#global vars
decimal_len = 3

def basic_calculator(a,b,operation):

  if (a.isnumeric() & b.isnumeric()):
    a=float(a)
    b=float(b)
    if operation == "add":
      result = a + b
    elif operation == "subtract":
      result = a - b
    elif operation == "divide":
      result = a / b
    elif operation == "multiply":
      result = a * b
    else:
      result = "Operations supported: add, subtract, divide, multiple only"
    
  else:
    result = "Please enter a valid number for a & b"
    

  return result

def strat_cost_calc(effort, cost):

  calc_cost = truncate_float((effort*effort)*cost,decimal_len)

  return calc_cost 

def prob_success_attack(e_a,e_d):
  prob = truncate_float((e_a/(1+e_d)), decimal_len)

  return prob

def calc_defender_payoff(prob_success, utility, cost):
  payoff = truncate_float(((1-prob_success)*utility) - cost, decimal_len)

  return payoff

def calc_attacker_payoff(prob_success, utility, cost):
  payoff = truncate_float(((prob_success)*utility) - cost, decimal_len)

  return payoff

def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier


def solve_game(payoffs_a, payoffs_d):
  gameN = nash.Game(payoffs_a,payoffs_d)
  gameN
  equilibria = gameN.support_enumeration()
  sol = []
  for eq in equilibria:
    sol.append(list(eq))

  arr1 = sol[0]
  #solve Utilities
  utility_arr = calc_utilities(payoffs_a, payoffs_d, sol[0])
  print(utility_arr)
  arr1.append(utility_arr)
  #format for html access; formats from tuple -> array values
  for x in range(len(arr1)):
    for y in range(len(arr1[x])):
      print("before " + str(arr1[x][y]))
      arr1[x][y] = truncate_float(arr1[x][y], decimal_len)
      print("after " + str(arr1[x][y]))

  return arr1

def calc_utilities(payoff_a, payoff_d, equilibria):
  attacker_utility = 0
  defender_utility= 0
  for i in range(2):
    for j in range(2):
      attacker_utility= attacker_utility + (equilibria[0][i]*payoff_a[i][j]*equilibria[1][j])
      defender_utility= defender_utility + (equilibria[1][i]*payoff_d[i][j]*equilibria[0][j])
  
  utility_arr = [attacker_utility, defender_utility]
  return utility_arr

def refactor_arrays_row(arr):
  arr1 = [arr[0], arr[1]]
  arr2 = [arr[2], arr[3]]
  
  newArr = [arr1, arr2]
  print(newArr)
  return newArr

def refactor_arrays_col(arr):
  arr1 = [arr[0], arr[2]]
  arr2 = [arr[1], arr[3]]
  
  newArr = [arr1, arr2]
  print(newArr)
  return newArr