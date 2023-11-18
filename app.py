
from flask import Flask, request, jsonify, render_template
import ast
import numpy as np
# Create the app object
app = Flask(__name__)


# importing function for calculations
from basic_calculator_function import basic_calculator
from basic_calculator_function import strat_cost_calc
from basic_calculator_function import prob_success_attack
from basic_calculator_function import calc_attacker_payoff
from basic_calculator_function import calc_defender_payoff
from basic_calculator_function import solve_game
from basic_calculator_function import refactor_arrays_row
from basic_calculator_function import refactor_arrays_col


# Define calculator
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    #get cost values from form
    active_cost_a = request.form['active_cost_a']
    passive_cost_a = request.form['passive_cost_a']
    defend_cost_d = request.form['defend_cost_d']
    no_cost_d = request.form['no_cost_d']

    costs_array = [float(active_cost_a),float(defend_cost_d),float(passive_cost_a),float(no_cost_d)]

    #get effort values from form
    active_effort_a = request.form['active_effort_a']
    passive_effort_a = request.form['passive_effort_a']
    defend_effort_d = request.form['defend_effort_d']
    no_effort_d = request.form['no_effort_d']
    
    effort_array=[float(active_effort_a),float(defend_effort_d),float(passive_effort_a),float(no_effort_d)]
    
    #get attacker utilities from form
    a11 = request.form['a11']
    a12 = request.form['a12']
    a21 = request.form['a21']
    a22 = request.form['a22']

    attacker_utility = [float(a11),float(a12),float(a21),float(a22)]
    
    #get defender utilities from form
    d11 = request.form['d11']
    d12 = request.form['d12']
    d21 = request.form['d21']
    d22 = request.form['d22']

    defender_utility = [float(d11),float(d12),float(d21),float(d22)]
    print("costs array " + str(costs_array))
    print("effort array " + str(effort_array))
    calc_cost_array = []
    #calculate costs for players
    for x in range(len(costs_array)):
        val = strat_cost_calc(effort_array[x], costs_array[x])
        calc_cost_array.append(val)

    print("calc_cost_arr " + str(calc_cost_array) )


    #calculate probs of success attack
    prob_success_array=[]
    effort_array_a = [effort_array[0], effort_array[2]]
    print("effort array a:" + str(effort_array_a))
    effort_array_d = [effort_array[1], effort_array[3]]
    print("effort array d:" + str(effort_array_d))
    for x in range(len(effort_array_a)):
        val= prob_success_attack(effort_array_a[x],effort_array_d[0])
        prob_success_array.append(val)
        val= prob_success_attack(effort_array_a[x],effort_array_d[1])
        prob_success_array.append(val)
    print("prob array: "+ str(prob_success_array))
    #calculate defender payoff
    calc_d_payoff_array = []
    calc_a_payoff_array = []
    for x in range(len(defender_utility)):
        print(x)
        if (x % 2) == 0:
            val = calc_defender_payoff(prob_success_array[x], defender_utility[x], calc_cost_array[1])
            print("defender val " + str(val))
            calc_d_payoff_array.append(val)
                
        else:
            val = calc_defender_payoff(prob_success_array[x], defender_utility[x], calc_cost_array[3])
            print("defender val " + str(val))
            calc_d_payoff_array.append(val)
    
    for x in range(len(attacker_utility)):
        print(x)
        if (x <2):
            val = calc_attacker_payoff(prob_success_array[x], attacker_utility[x], calc_cost_array[0])
            print("prob val " + str(prob_success_array[x]) + " attacker_utility: " + str(attacker_utility[x]) + " calc_cost_array: "+ str(calc_cost_array[0]))
            print("attacker val " + str(val))
            calc_a_payoff_array.append(val)
                
        else:
            val = calc_attacker_payoff(prob_success_array[x], attacker_utility[x], calc_cost_array[2])
            print("prob val " + str(prob_success_array[x]) + " attacker_utility: " + str(attacker_utility[x]) + " calc_cost_array: "+ str(calc_cost_array[2]))
            print("attacker val " + str(val))
            calc_a_payoff_array.append(val)
                
                

    
    #result = basic_calculator(a,b,operation)

    calc_list = [effort_array, calc_cost_array, prob_success_array, calc_a_payoff_array, calc_d_payoff_array]
    result=1+2
    return render_template('results.html', calc_list = calc_list )

@app.route('/test',methods=['POST'])
def results():

    calc_list = request.form['selected_items']
    calc_list_array = ast.literal_eval(calc_list)
    attacker_payoffs = calc_list_array[3]
    defender_payoffs = calc_list_array[4]

    
    rowPlayer = refactor_arrays_row(attacker_payoffs)
    colPlayer = refactor_arrays_col(defender_payoffs)

    solution = solve_game(rowPlayer, colPlayer)
    
    solution.append(attacker_payoffs)
    solution.append(defender_payoffs)
    return render_template('solution.html', solution=solution)

if __name__ == "__main__":
    app.run(debug=True) 
