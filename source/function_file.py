import csv
import numpy as np
from scipy.optimize import minimize
import random


def read_csv(filename,duration):                                    # still using a single load pattern for all houses
    """Reads in load and generation data from data set"""
    with open(filename) as csvfile:
        CSVread = csv.reader(csvfile, delimiter=',')
        data_return = np.array([])
        for row in CSVread:
            data_value = float(row[-1])
            data_return = np.append(data_return, data_value)
        while len(data_return) < duration:
            data_return = np.append(data_return, 0)
        return data_return


def define_pool(consumption_at_round, production_at_round):
    """this function has to decide whether agent is a buyer or a seller"""
    surplus_per_agent = production_at_round - consumption_at_round
    if surplus_per_agent > 0:
        classification = "seller"
        demand_agent = 0
    elif surplus_per_agent < 0:
        classification = "buyer"
        demand_agent = abs(surplus_per_agent)
        surplus_per_agent = 0
    else:
        classification = "passive"
    return [classification, surplus_per_agent, demand_agent]


def calc_supply(surplus_per_agent, w_j_storage_factor):             # E_j
    supply_per_agent = surplus_per_agent * w_j_storage_factor
    return supply_per_agent


def allocation_to_i_func(supply_on_step, bidding_price_i, bidding_prices_total):            # w_j_storage_factor is nested in E_total_supply
    Ei = supply_on_step*(bidding_price_i/bidding_prices_total)
    return Ei


def calc_R_j_revenue(R_total, E_j_supply, w_j_storage_factor, E_total_supply):
    """calculation of revenue for seller j depending on allocation to i"""
    R_j = R_total * (E_j_supply*w_j_storage_factor)/E_total_supply    # payment_i is E_i*ci = amount of demanded energy * bidding price
    return R_j


def calc_utility_function_i(supply_on_step, c_macro, bidding_price_i, bidding_prices_summed):
    """This function calculates buyers utility"""
    E_i_allocation = allocation_i(supply_on_step,bidding_price_i, bidding_prices_summed)
    utility_i = E_i_allocation * (c_macro[1] - bidding_price_i)
    return utility_i


def calc_utility_function_j(id, R_total, E_j_supply, w_j_storage_factor, E_total_supply):
    """This function calculates sellers utility"""
    R_j_revenue = calc_R_j_revenue(R_total, E_j_supply, w_j_storage_factor, E_total_supply)
    utility_j = E_j_supply*(1 - w_j_storage_factor) + R_j_revenue  # utility of selling agent j
    return utility_j


def allocation_i(supply_on_step,bidding_price_i, bidding_prices_all):
    E_i_allocation = supply_on_step * (bidding_price_i / bidding_prices_all)
    return E_i_allocation


def calc_gamma():
    return random.uniform(0, 1)
    """This function will ultimately predict storage weight
    This will involve some model predictive AI"""


def buyers_game_optimization(id_buyer, E_i_demand ,supply_on_step, c_macro, bidding_price_i_prev, bidding_prices_all):
    """Level 1 game: distributed optimization"""

    E_i_allocation_optimization = allocation_i(supply_on_step, bidding_price_i_prev, bidding_prices_all)
    print("allocation to buyer =", E_i_allocation_optimization)

    """globally declared variables, do not use somewhere else!!"""
    global E_global_buyers, c_S_global_buyers, c_i_global_buyers, c_l_global_buyers, E_i_demand_global
    E_global_buyers = supply_on_step
    c_S_global_buyers = c_macro[1]
    c_l_global_buyers = bidding_prices_all
    c_i_global_buyers = bidding_price_i_prev
    E_i_demand_buyers_global = E_i_demand

    initial_conditions = [E_global_buyers, c_S_global_buyers, c_l_global_buyers, c_i_global_buyers, E_i_demand_buyers_global]

    def utility_buyer(x, sign=-1):
        x0 = x[0]   # E_global_buyers
        x1 = x[1]   # c_S_global_buyers
        x2 = x[2]   # c_l_global_buyers
        x3 = x[3]   # c_i_global_buyers               unconstrained
        x4 = x[4]   # E_i_demand_buyers_global

        """self designed parametric utility function"""
        return x4 * x1 - (x0 * (x3 / x2)) * x3 + (x4 - (x0 * (x3 / x2))) * x1

        """original utility function, minimizes """
        # return sign*x0*(x3/x2)*x1 - x0*(x3/x2)*x3

    """fix parameters E_global, c_S_global, c_l_global"""
    def constraint_param_x0(x):
        return E_global_buyers - x[0]

    def constraint_param_x1(x):
        return c_S_global_buyers - x[1]

    def constraint_param_x2(x):
        return c_l_global_buyers - x[2]

    def constraint_param_x4(x):
        return E_i_demand_buyers_global - x[4]

    """incorporate various constraints"""
    con0 = {'type': 'eq', 'fun': constraint_param_x0}
    con1 = {'type': 'eq', 'fun': constraint_param_x1}
    con2 = {'type': 'eq', 'fun': constraint_param_x2}
    con4 = {'type': 'eq', 'fun': constraint_param_x4}

    cons = [con0, con1, con2, con4]
    # bounds_buyer = ((0, None), (0, None), (0, None), (c_macro[0], c_macro[1]), (0, None))
    bounds_buyer = ((0, None), (0, None), (0, None), (c_macro[0], None), (0, None))

    """optimize using SLSQP(?)"""
    sol_buyer = minimize(utility_buyer, initial_conditions, method='SLSQP', bounds=bounds_buyer, constraints=cons)
    # print("optimization result is a bidding price of %f" % sol.x[3])
    print("buyer %d game results in %s" % (id_buyer, sol_buyer.x[3]))

    """return 4th element of solution vector."""
    return sol_buyer, sol_buyer.x[3]


def sellers_game_optimization(id_seller, total_offering, supply_energy_j, total_supply_energy, gamma, w_j_storage_factor):
    """ Anticipation on buyers is plugged in here"""
    gamma = 1
    global Ej_global_sellers, R_total_global_sellers, gamma_global_sellers, E_global_sellers, wj_global_sellers
    Ej_global_sellers = supply_energy_j
    R_total_global_sellers = total_offering
    gamma_global_sellers = gamma
    E_global_sellers = total_supply_energy
    wj_global_sellers = w_j_storage_factor

    initial_conditions_seller = [Ej_global_sellers, R_total_global_sellers, gamma_global_sellers, E_global_sellers, wj_global_sellers]

    def utility_seller(x, sign= -1):
        x0 = x[0]  # Ej_global_sellers
        x1 = x[1]  # R_total_global_sellers
        x2 = x[2]  # gamma_global_sellers
        x3 = x[3]  # E_global_sellers
        x4 = x[4]  # wj_global_sellers

        return sign * x0 * (1 - x4**(1.7)) + x2 * x1 * ((x0 * x4) / x3)

    def constraint_param_seller0(x):
        return Ej_global_sellers - x[0]

    def constraint_param_seller1(x):
        return R_total_global_sellers - x[1]

    def constraint_param_seller2(x):
        return gamma_global_sellers - x[2]

    def constraint_param_seller3(x):
        return E_global_sellers - x[3]

    """incorporate various constraints"""
    con_seller0 = {'type': 'eq', 'fun': constraint_param_seller0}
    con_seller1 = {'type': 'eq', 'fun': constraint_param_seller1}
    con_seller2 = {'type': 'eq', 'fun': constraint_param_seller2}
    con_seller3 = {'type': 'eq', 'fun': constraint_param_seller3}
    cons_seller = [con_seller0, con_seller1, con_seller2, con_seller3]
    bounds_seller = ((0, None), (0, None), (0, None), (0, None), (0, 1))

    sol_seller = minimize(utility_seller, initial_conditions_seller, method='SLSQP', bounds=bounds_seller, constraints=cons_seller)  # bounds=bounds
    print("seller %d game results in %s" % (id_seller, sol_seller.x[4]))

    """return 5th element of solution vector."""
    return sol_seller, sol_seller.x[4]
    pass





"""testing c_i within domain C_i
if c_i_price_vector in possible_c_i:
    print("all fine")
else:
    print("macro-grid is competing")

"""






