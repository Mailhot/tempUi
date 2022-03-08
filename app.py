import streamlit as st
import time
import numpy as np

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)


st.title('Smoking temperature logger.')
placeholder = st.empty()
temperature1 = 0
# with container1:
#     col1, col2 = st.columns(2)
#     col1.metric(label="Grill Temp", value=str(temperature1) + " °C", delta="1.2 °C")
#     col2.metric(label="Meat Temp", value="0 °C", delta="-1.2 °C")

    


chart = st.line_chart(last_rows)



for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    temperature1 += 1
    
    placeholder.empty()
    with placeholder.container():

        col1, col2 = st.columns(2)

        col1.metric(label="Grill Temp", value=str(temperature1) + " °C", delta="1.2 °C")
        col2.metric(label="Meat Temp", value=str(temperature1 *2) + " °C", delta="-1.2 °C")

    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(1)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")