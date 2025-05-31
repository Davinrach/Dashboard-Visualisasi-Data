import time
import numpy as np  
import pandas as pd
import plotly.express as px
import streamlit as st

# Read CSV from a GitHub repo
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# Memoize data loading for efficiency
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

# Load data
df = get_data()














# st.text_input('your name', key = 'name')
# st.write(f'hello {st.session_state.name}')

# number = st.number_input('enter a number')
# st.write('the current number is ', number)

# if st.button('submit'):
#     st.write('You Submitted: ')
# else: 
#     st.write('You have not submitted yet.')

# agree = st.checkbox('I Agree')
# disagree = st.checkbox('I Disagree')
# if agree : 
#     st.write('Great!!!!')

# skill_option = st.selectbox('select your programming language', ['Java', 'C'])
# st.write('You Selected', skill_option) 

# score = st.slider('What is your score', 0, 100, (80))
# st.write('your score is', score)

# add_selectbox = st.sidebar.selectbox('which number do you like?', [10,20,30,40,50])

# df = pd.DataFrame(np.random.rand(10,3),
#     columns=('column %d'% col
#     for col in range(3)))
# column_left, column_right = st.columns(2)

# with column_left: 
#     st.line_chart(data=df)
# with column_right:
#     st.write(df)

    