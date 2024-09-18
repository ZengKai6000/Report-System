from sql_connections import sql_connections
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import xlsxwriter
import numpy as np
import math

def lossf(contract, demand):
    if demand > 1.1 * contract:
        return 3 * (demand - 1.1 * contract) + 2 * 0.1 * contract
    elif demand > contract:
        return demand - contract
    else:
        return contract - demand

def main():
    """test data info"""
    device_id = '06389897047_010se'
    contract_upperLimit = 49
    contract_lowerLimit = 0
    obsered_weeks = 4

    """"""
    now = datetime.now()
    start_date = datetime.now() - timedelta(weeks=obsered_weeks, hours=datetime.now().hour, minutes=datetime.now().minute+1)

    connector_device = sql_connections('196', 'ima_thing')
    query = "SELECT id,kw FROM ima_thing.%s WHERE id BETWEEN '%s' and '%s'" %(device_id, start_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
    demand_data = connector_device.sql(query)
    max_kw = []
    temp_list = []
    temp = 0
    for i in demand_data:
        if len(temp_list) < 15 and i[1]:
            temp_list.append(i[1])
        elif i[1]:
            temp_list.append(i[1])
            del temp_list[0]
            temp = max(temp, sum(temp_list)/15 or 0)
        if i[0] - start_date >= timedelta(days=1):
            start_date += timedelta(days=1)
            max_kw.append(temp)
            temp = 0
            temp_list = []
        
    lowest_loss = math.inf
    best_contract = 0
    for i in range(contract_lowerLimit, contract_upperLimit + 1):
        loss = 0
        for j in range(len(max_kw)):
            loss += lossf(i, float(max_kw[j]))
        if loss <=lowest_loss:
            lowest_loss = loss
            best_contract = i
    #print("Best Contract = %d" %best_contract)
    print(max(max_kw))
    plt.xlabel("Days")
    plt.ylabel("kw")
    plt.title(device_id)
    plt.scatter(np.linspace(1, len(max_kw), num=len(max_kw)), max_kw)
    #plt.plot(np.linspace(1, len(max_kw), num=len(max_kw)), np.linspace(best_contract, best_contract, num=len(max_kw)))
    plt.show()
    












if __name__ == '__main__':
    main()