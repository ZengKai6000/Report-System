from sql_connections import sql_connections
import pandas as pd
connector_device = sql_connections('195', 'temp')

query = "SELECT place_id FROM temp.ima_bill_view where status = 1 or status = 2;"

contract_list = connector_device.sql(query=query)
contract_list = [x[0] for x in contract_list]

test_db = ['195', '196']

data = pd.DataFrame(columns = ["DeviceID", "Last Connection"])
for db in test_db:
    connector_device = sql_connections(db, 'ima_thing')

    query = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA = 'ima_thing' and TABLE_NAME like '___________\______';"

    device_list = connector_device.sql(query=query)

    

    success = 0
    fail = 0
    for i in device_list:  
        try:
            query = "SELECT id from ima_thing.%s order by id desc limit 1" %i[0]
            record = connector_device.sql(query=query)
            if i[0][:11] in contract_list:
                data = pd.concat([data, pd.DataFrame({"DeviceID": i, "Last Connection": record[0]})])
            success += 1
            print("Progress: %d/%d, fail: %d" %(success, len(device_list), fail))
        except Exception:
            fail += 1
            print("Progress: %d/%d, fail: %d" %(success, len(device_list), fail))
            continue

data.to_excel("Connection.xlsx")