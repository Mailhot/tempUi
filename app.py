import streamlit as st
import time
import numpy as np
import pandas as pd
import time
import csv

# Communicate with Arduino board
import serial
ser = serial.Serial('/dev/ttyUSB0')
ser.flushInput()

device_addresses = {'3BAADF410BF40DF1': 'grill_temp',
                    '3BE5EC410BF42D49': 'meat_temp',
                    }
filename = "log_" + str(time.time()) + ".csv"
last_rows = []
st.title('Smoking temperature logger.')
placeholder = st.empty()
grill_temp_diff = 0
meat_temp_diff = 0

data = pd.DataFrame([[20.0,20.0]], columns=['Grill', 'Meat1'])

# Persistent session data
if 'df' not in st.session_state:
    st.session_state.df = data

chart = st.line_chart(data)
# table = st.dataframe(data)

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    except KeyboardInterrupt:
        break
    except:
        print('error decoding skipping')
        break
    print(decoded_bytes)
    result = decoded_bytes.strip().split(' ')
    # print(result)
    if len(result) == 6:
        address1, _, temp1, address2, _, temp2 = result
        # device = device_addresses.get(device_address)
        # print(device, temp_c)
    

        with open(filename,"a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([time.time(), address1, temp1, address2, temp2])
        new_rows = pd.DataFrame([[float(temp1), float(temp2)]], columns=['Grill', 'Meat1'])
        st.session_state.df = st.session_state.df.append(new_rows, ignore_index=True)
        if len(st.session_state.df.index) > 51:
            # print(st.session_state.df.iloc[-50]['Grill'])
            grill_temp_diff = float(temp1) - st.session_state.df.iloc[-50]['Grill']
            meat_temp_diff = float(temp2) - st.session_state.df.iloc[-50]['Meat1']
        elif len(st.session_state.df.index) > 6:
            # print(st.session_state.df.iloc[-1]['Grill'])
            grill_temp_diff = float(temp1) - st.session_state.df.iloc[-5]['Grill']
            meat_temp_diff = float(temp2) - st.session_state.df.iloc[-5]['Meat1']
        chart.add_rows(new_rows)
        # table.add_rows(new_rows)
        # print(last_rows)

    else:
        continue    
        
    placeholder.empty()
    with placeholder.container():

        col1, col2 = st.columns(2)


        col1.metric(label="Grill Temp", value=str(temp1) + " ??C", delta=str(grill_temp_diff) + " ??C")
        col2.metric(label="Meat Temp", value=str(temp2) + " ??C", delta=str(meat_temp_diff) + " ??C")

    # progress_bar.progress(i)
    # last_rows = new_rows
    time.sleep(1)

# progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")