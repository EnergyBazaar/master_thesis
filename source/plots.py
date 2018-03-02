import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import numpy as np

def close_all():
    plt.close("all")

def plot_E_total_surplus_prediction_per_step(E_total_surplus_prediction_per_step, N):
    # plt.plot(E_total_surplus_prediction_per_step/N)
    return


def plot_prediction(means_surplus, means_load):
    # plt.title('mean of surplus and load')
    # plt.plot(means_surplus)
    # plt.plot(means_load)
    return


def plot_results(mean_sharing_factors, supply_over_time_list, demand_over_time, c_nominal_over_time, buyers, sellers):

    fig_control_values = plt.figure(figsize=(10,7))
    ax1 = fig_control_values.add_subplot(221)
    ax2 = fig_control_values.add_subplot(224)
    ax3 = fig_control_values.add_subplot(223)
    ax4 = fig_control_values.add_subplot(222)


    ax1.plot(supply_over_time_list, label="supply_over_time_list")
    ax1.plot(demand_over_time, label="demand_over_time")
    ax1.set_title('supply/demand over time')

    ax2.plot(mean_sharing_factors, label="mean_sharing_factors")
    ax2.set_title('mean sharing factor per step')

    ax3.plot(c_nominal_over_time, label="c_nominal_over_time")
    ax3.set_title('bidding price over time')

    ax4.plot(buyers, label="buyers")
    ax4.plot(sellers, label="sellers")
    ax4.set_title('sellers/buyers pool')

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()


    plt.suptitle('Results')
    fig_control_values.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_control_values.pdf', bbox_inches='tight')  # save the figure to file


def plot_w_nominal_progression(w_nominal_over_time, R_prediction_over_time, E_prediction_over_time, E_real_over_time, R_real_over_time, c_nominal):
    """w_nominal against predicted energy and predicted revenue"""

    # R_prediction_over_time_normalised = R_prediction_over_time/max(R_prediction_over_time)
    # E_prediction_over_time_normalised = E_prediction_over_time/max(E_prediction_over_time)
    # E_real_over_time_normalised = E_real_over_time/max(E_real_over_time)
    # R_real_over_time_normalised = R_real_over_time/max(R_real_over_time)

    fig_w_nominal_progression = plt.figure(figsize=(10,10))
    ax1 = fig_w_nominal_progression.add_subplot(211)
    ax1.plot(w_nominal_over_time, label='w_nominal')
    ax1.plot(E_prediction_over_time, label='E_prediction (weighted)')
    ax1.plot(c_nominal, label='c_nominal')
    ax1.plot(E_real_over_time, label='E_real')
    ax1.set_title('Energy surplus real vs prediction model')
    ax1.legend()


    ax2 = fig_w_nominal_progression.add_subplot(212)
    ax2.plot(w_nominal_over_time, label='w_nominal')
    ax2.plot(R_prediction_over_time, label='R_prediction (weighted)')
    ax2.plot(R_real_over_time, label='R_real')
    ax1.set_title('Revenue real vs prediction model')
    ax2.legend()

    plt.suptitle('Normalised data on trading')

    """normalised"""
    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(211)
    # ax1.plot(w_nominal_over_time, label='w_nominal')
    # ax1.plot(E_prediction_over_time_normalised, label='E_prediction')
    # ax1.plot(E_real_over_time_normalised, label='E_real')
    # ax1.set_title('Energy surplus real vs prediction model')
    # ax1.legend()
    #
    #
    # ax2 = fig1.add_subplot(212)
    # ax2.plot(w_nominal_over_time, label='w_nominal')
    # ax2.plot(R_prediction_over_time_normalised, label='R_prediction')
    # ax2.plot(R_real_over_time_normalised + 1, label='R_real')
    # ax1.set_title('Revenue real vs prediction model')
    # ax2.legend()
    #
    # plt.suptitle('Normalised data on trading')
    # #plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)
    fig_w_nominal_progression.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_w_nominal_progression.pdf', bbox_inches='tight')  # save the figure to file


def plot_available_vs_supplied(actual_batteries_over_time, E_total_supply_over_time, E_demand_over_time, N):

    fig_available_vs_supplied = plt.figure(figsize=(10,7))
    ax1 = fig_available_vs_supplied.add_subplot(211)
    ax1.plot(E_demand_over_time, label='Demanded by buyers')
    ax1.plot(E_total_supply_over_time, label='Supplied by sellers')
    ax1.set_title('Demanded vs Supplied')
    ax1.legend()

    batt_soc_ax2 = fig_available_vs_supplied.add_subplot(212)
    for agent in range(N):
        batt_soc_ax2.plot(actual_batteries_over_time[agent], label='soc agent %d' % agent)
    batt_soc_ax2.set_title('State-of-Charge batteries per agent')
    batt_soc_ax2.legend()

    plt.suptitle('battery business')
    fig_available_vs_supplied.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_available_vs_supplied.pdf', bbox_inches='tight')  # save the figure to file


def plot_supplied_vs_surplus_total(surplus_on_step_over_time, supplied_on_step_over_time, demand_on_step_over_time):

    fig_supplied_vs_surplus_total = plt.figure(figsize=(10,7))

    ax1 = fig_supplied_vs_surplus_total.add_subplot(211)
    ax1.plot(surplus_on_step_over_time, label='surplus energy in the system')
    ax1.plot(supplied_on_step_over_time, label='supplied in the system')
    ax1.plot(demand_on_step_over_time, label='demand in the system')
    ax1.legend()
    ax1.set_title('energy availability')

    fig_supplied_vs_surplus_total.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_supplied_vs_surplus_total.pdf', bbox_inches='tight')  # save the figure to file

def plot_utility_buyer(utilities_buyers_over_time, c_prices_over_time, E_total_demand_over_time, E_surplus_over_time, E_total_supply, c_nominal_over_time, N, steps):

    utilities_buyers_total_series = np.zeros(steps)
    utilities_buyers_demand_gap_series = np.zeros(steps)
    utilities_buyers_costs_series = np.zeros(steps)

    fig_buyers = plt.figure(figsize=(10,7))
    ax1 = fig_buyers.add_subplot(311)

    for agent in range(N):

        for i in range(steps):
            utilities_buyers_total_series[i] = utilities_buyers_over_time[i][agent][0]
            utilities_buyers_demand_gap_series[i] = utilities_buyers_over_time[i][agent][2]
            utilities_buyers_costs_series[i] = utilities_buyers_over_time[i][agent][3]

        ax1.plot(utilities_buyers_total_series, label='Utility buyers total')
        ax1.plot(utilities_buyers_demand_gap_series, label='Utility buyers demand gap')
        ax1.plot(utilities_buyers_costs_series, label='Utility buyers costs')
    ax1.set_title('plotted utility buyers')

    ax2 = fig_buyers.add_subplot(312)
    ax2.plot(c_nominal_over_time, label="c_nominal_over_time")
    ax2.set_title('bidding price over time')

    ax3 = fig_buyers.add_subplot(313)
    for agent in range(N):
        E_demand_agent_series = np.zeros(steps)
        for i in range(steps):
            E_demand_agent_series[i] =  E_total_demand_over_time[agent][i]

        ax3.plot(E_demand_agent_series, label="E_demand per agent")
    ax3.set_title('energy demand over time')

    ax1.legend()
    ax2.legend()
    ax3.legend()

    plt.suptitle('utility buyer')
    fig_buyers.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_buyers.pdf', bbox_inches='tight')  # save the figure to file

def plot_utility_seller(utilities_sellers_over_time, w_factors_over_time, E_total_demand_over_time, w_nominal_over_time, N, steps):

    utilities_sellers_total_series = np.zeros(steps)
    utilities_buyers_demand_gap_series = np.zeros(steps)
    utilities_buyers_costs_series = np.zeros(steps)

    fig_buyers = plt.figure(figsize=(10,7))
    ax1 = fig_buyers.add_subplot(311)

    for agent in range(N):

        for i in range(steps):
            utilities_buyers_total_series[i] = utilities_buyers_over_time[i][agent][0]
            utilities_buyers_demand_gap_series[i] = utilities_buyers_over_time[i][agent][2]
            utilities_buyers_costs_series[i] = utilities_buyers_over_time[i][agent][3]

        ax1.plot(utilities_buyers_total_series, label='Utility buyers total')
        ax1.plot(utilities_buyers_demand_gap_series, label='Utility buyers demand gap')
        ax1.plot(utilities_buyers_costs_series, label='Utility buyers costs')
    ax1.set_title('plotted utility buyers')

    ax2 = fig_buyers.add_subplot(312)
    ax2.plot(c_nominal_over_time, label="c_nominal_over_time")
    ax2.set_title('bidding price over time')

    ax3 = fig_buyers.add_subplot(313)
    ax3.plot(demand_in_grid_over_time, label="E_demand")
    ax3.set_title('energy demand over time')

    ax1.legend()
    ax2.legend()
    ax3.legend()

    plt.suptitle('utility buyer')



def plot_utilities(utilities_buyers_over_time, utilities_sellers_over_time, N, steps): #utility_buyers_over_time[N][3][sim_steps]

    utilities_sellers_over_time_1 = np.zeros(steps)
    utilities_sellers_over_time_2 = np.zeros(steps)
    utilities_sellers_over_time_3 = np.zeros(steps)

    utilities_buyers_total_series = np.zeros(steps)
    utilities_buyers_demand_gap_series = np.zeros(steps)
    utilities_buyers_costs_series = np.zeros(steps)

    fig_utilities = plt.figure(figsize=(10,7))

    ax1 = fig_utilities.add_subplot(211)
    for agent in range(N):
        """[agent.utility_j, prediction_utility, direct_utility]"""
        for i in range(steps):
            utilities_sellers_over_time_1[i] = utilities_sellers_over_time[i][agent][0] # utility_j
            utilities_sellers_over_time_2[i] = utilities_sellers_over_time[i][agent][1] # prediction_utility
            utilities_sellers_over_time_3[i] = utilities_sellers_over_time[i][agent][2] # direct_utility

        # ax1.plot(utilities_sellers_over_time_1, label='Utility sellers total' + str(int(agent)))
        # ax1.plot(utilities_sellers_over_time_2, label='Utility sellers prediction part' + str(int(agent)))
        # ax1.plot(utilities_sellers_over_time_3, label='Utility sellers direct part' + str(int(agent)))

        ax1.plot(utilities_sellers_over_time_1, label='Utility sellers total' + str(int(agent)))

        # ax1.plot(utilities_sellers_over_time[:][agent][1], label='Utility sellers total' + str(int(agent)))
        # ax1.plot(utilities_sellers_over_time[:][agent][2], label='Utility sellers prediction part' + str(int(agent)))
        # ax1.plot(utilities_sellers_over_time[:][agent][3], label='Utility sellers direct part' + str(int(agent)))

    ax1.set_title('plotted utility sellers')
    ax1.legend()

    ax2 = fig_utilities.add_subplot(212)
    for agent in range(N):

        for i in range(steps):
            utilities_buyers_total_series[i] = utilities_buyers_over_time[i][agent][0]
            utilities_buyers_demand_gap_series[i] = utilities_buyers_over_time[i][agent][2]
            utilities_buyers_costs_series[i] = utilities_buyers_over_time[i][agent][3]

        ax2.plot(utilities_buyers_total_series, label='Utility buyers total')
        ax2.plot(utilities_buyers_demand_gap_series, label='Utility buyers demand gap')
        ax2.plot(utilities_buyers_costs_series, label='Utility buyers costs')
    ax2.set_title('plotted utility buyers')
    ax2.legend()

    plt.suptitle('Utility values Buyers/Sellers')
    fig_utilities.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_utilities_both.pdf', bbox_inches='tight')  # save the figure to file

    # ax2 = fig_utilities.add.subplot(212)

def plot_avg_soc_preferred(actual_batteries_over_time, soc_preferred_list_over_time, avg_soc_preferred_over_time, soc_actual_over_time, deficit_total_over_time, deficit_total_progress_over_time, production_series_total, N, steps):



    fig_soc_preferred = plt.figure(figsize=(10,5))
    ax1 = fig_soc_preferred.add_subplot(311)
    ax2 = fig_soc_preferred.add_subplot(312)
    ax3 = fig_soc_preferred.add_subplot(313)

    avg_deficit_total_over_time = deficit_total_over_time / N

    avg_soc_actual_over_time = np.zeros(steps)
    for agent in range(N):
        for i in range(steps):
            avg_soc_actual_over_time[i] += soc_actual_over_time[agent][i]/N

    ax1.plot(avg_soc_preferred_over_time, label='average soc_preferred over time')
    ax1.plot(avg_soc_actual_over_time, label='average soc_actual over time')
    ax1.plot(avg_deficit_total_over_time, label='total deficit on each step')
    # ax1.plot(production_series_total, alpha=0.5, label='total production over time')


    # std_soc_preferred_list_over_time = np.std(soc_preferred_list_over_time, axis=0)
    # std_actual_batteries_over_time = np.std(actual_batteries_over_time, axis=0)
    # min_soc_preferred_list_over_time = min(soc_preferred_list_over_time, axis=0)
    # max_soc_preferred_list_over_time = max(soc_preferred_list_over_time, axis=0)
    # min_actual_batteries_over_time = min(actual_batteries_over_time, axis=0)
    # max_actual_batteries_over_time = max(actual_batteries_over_time, axis=0)

    for i in range(N):
        ax2.plot(soc_preferred_list_over_time[i], label='soc_preferred for agent' + str(i))

    for i in range(N):
        ax3.plot(actual_batteries_over_time[i], label='soc_actual for agent' + str(i))

    ax1.legend()

    ax1.set_title('averages')
    ax2.set_title('preferred soc for each agent')
    ax3.set_title('actual soc for each agent')

    fig_soc_preferred.show()
    fig_soc_preferred.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_soc_preferred.pdf', bbox_inches='tight')  # save the figure to file

def plot_supply_demand(E_total_supply, E_actual_supplied_total, demand_in_grid_over_time, N):

    fig_supply_demand = plt.figure(figsize=(5,5))
    ax1 = fig_supply_demand.add_subplot(111)

    ax1.plot(E_total_supply, label='Total available supply')
    ax1.plot(E_actual_supplied_total, label='Total actual supply')
    ax1.plot(demand_in_grid_over_time, label='Total demand')

    ax1.legend()
    plt.suptitle('Supply vs Demand')

    fig_supply_demand.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_supply_demand.pdf', bbox_inches='tight')  # save the figure to file

# def soc_households():
#
#     soc_households = plt.figure(figsize=(10,10))
#     avg = soc_households.add_subplot(211)
#     agents = soc_households.add_subplot(212)



def plot_input_data(big_data_file, sim_steps,N):

    fig_input_data = plt.figure(figsize=(10,10))
    ax1 = fig_input_data.add_subplot(311)
    ax2 = fig_input_data.add_subplot(312)
    ax3 = fig_input_data.add_subplot(313)

    load_series = np.zeros(sim_steps)
    production_series = np.zeros(sim_steps)

    load_series_total = np.zeros(sim_steps)
    production_series_total = np.zeros(sim_steps)

    for agent in range(N):
        max_consumption = max(big_data_file[:][agent][0])

        for i in range(sim_steps):
            load_series[i] = big_data_file[i][agent][0]
            production_series[i] = big_data_file[i][agent][1]
            load_series_total[i] += load_series[i]
            production_series_total[i] += production_series[i]

        ax1.plot(load_series, label='load of agent' + str(int(agent)))
        ax2.plot(production_series, label='production of agent' + str(int(agent)))

    ax3.plot(load_series_total, label='total load')
    ax3.plot(production_series_total, label='total production')



    ax1.set_title('consumption per agent')
    ax2.set_title('production per agent')
    ax3.set_title('total production and total consumption')
    ax3.legend()

    plt.suptitle('Supply vs Demand')
    fig_input_data.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_input_data.pdf', bbox_inches='tight')  # save the figure to file


    load = sum(load_series_total)
    production = sum(production_series_total)

    return load, production, load_series_total, production_series_total


def plot_C_P(load_series_total, production_series_total):
    fig_total_P_C = plt.figure(figsize=(20,5))
    plt.plot(load_series_total, label='total production')
    plt.plot(production_series_total, label='total production')

    x_position = [1,2,3,4,5]
    for i in range(len(x_position)):
        plt.axvline(x_position[i]*144, color='k', linestyle='--', alpha=0.3)

    plt.legend()
    plt.suptitle('Total Production vs. Consumption')
    fig_total_P_C.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_total_P_C.pdf', bbox_inches='tight')  # save the figure to file

    return

def plot_iterations(global_iteration_over_time, buyer_iteration_over_time, seller_iteration_over_time):

    fig_plot_iterations = plt.figure(figsize=(20,5))

    plt.plot(global_iteration_over_time, label='global-level iterations')
    plt.plot(buyer_iteration_over_time, label='buyers-level iterations')
    plt.plot(seller_iteration_over_time, label='sellers-level iterations')

    fig_plot_iterations.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_plot_iterations.pdf', bbox_inches='tight')  # save the figure to file



def plot_profits(profit_list_over_time, profit_list_summed_over_time, N):

    fig_plot_profits = plt.figure(figsize=(20,5))
    # for agent in range(N):
    #     plt.plot(profit_list_over_time[agent][:], label='profits')

    plt.plot(profit_list_summed_over_time)


    fig_plot_profits.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_plot_profits.pdf', bbox_inches='tight')  # save the figure to file

def plot_costs_over_time(E_demand_list_over_time, E_allocated_list_over_time, payment_list, E_total_supply_list_over_time, E_actual_supplied_list, revenue_list, N, steps):
    """ Costs over time """

    """ Zooms in on 1 agent over time"""
    fig_costs_over_time_agent = plt.figure(figsize=(20,5))
    sales = fig_costs_over_time_agent.add_subplot(311)
    buys = fig_costs_over_time_agent.add_subplot(312)
    profit = fig_costs_over_time_agent.add_subplot(313)

    agent = [3]

    for i in range(len(agent)):
        buys.plot(E_demand_list_over_time[agent[i]][:],label='demand agent'  + str(agent[i]))
        buys.plot(E_allocated_list_over_time[agent[i]][:],label='allocated to agent' + str(agent[i]))

        sales.plot(E_total_supply_list_over_time[agent[i]][:],label='supply from agent' + str(agent[i]))
        sales.plot(E_actual_supplied_list[agent[i]][:],label='actually supplied from agent' + str(agent[i]))

        buys.plot(payment_list[agent[i]][:], label='payments from agent' + str(agent[i]))
        sales.plot(revenue_list[agent[i]][:], label='revenue to agent' + str(agent[i]))

    balance_over_time = np.zeros(steps)
    for i in range(len(agent)):
        balance = 0
        for step in range(steps):
            balance += revenue_list[agent[i]][step] - payment_list[agent[i]][step]
            balance_over_time[step] = balance

    profit.plot(balance_over_time, label = 'balance per agent')

    buys.legend()
    sales.legend()

    buys.set_title('buys over time per agent')
    sales.set_title('sales over time per agent')

    profit.set_title('profit over time per agent')
    fig_costs_over_time_agent.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_costs_over_time_agent.pdf', bbox_inches='tight')  # save the figure to file


def plot_PSO(results_over_time, P_supply_list_over_time, P_demand_list_over_time, gen_output_list_over_time, load_demand_list_over_time, avg_battery_soc_list_over_time, N, sim_steps):

    fig_plot_PSO_dispatch = plt.figure(figsize=(20,5))
    ax1 = fig_plot_PSO_dispatch.add_subplot(211)
    ax2 = fig_plot_PSO_dispatch.add_subplot(212)

    total_supply_on_step = np.zeros(sim_steps)
    for step in range(sim_steps):
        supply_per_agent_on_step = 0
        for agent in range(N):
            supply_per_agent_on_step += results_over_time[agent][step]
        total_supply_on_step[step] = supply_per_agent_on_step
        # ax1.plot(results_over_time[agent][:])

    ax1.plot(total_supply_on_step, label='Generator dispatch optimized')
    ax1.plot(P_supply_list_over_time, label='Generator dispatch maximum')
    ax1.plot(P_demand_list_over_time, label='Demand of households total')

    ax2.plot(gen_output_list_over_time, label='gen_output_list_over_time')
    ax2.plot(load_demand_list_over_time, label='load_demand_list_over_time')
    ax2.plot(avg_battery_soc_list_over_time, label='mean battery over time')

    plt.legend()

    fig_plot_PSO_dispatch.savefig('/Users/dirkvandenbiggelaar/Desktop/python_plots/fig_plot_PSO_dispatch.pdf', bbox_inches='tight')  # save the figure to file


""" TODO 

prediction analyseren
congestion set-up maken


"""
