# %%
import dash
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
import time as time_pck
import os
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from app import app
import streamlit as st
from datetime import time
from Filters import filter_A, filter_CD

os.chdir(r"C:\Users\Lior\Desktop\Information-Visualization")

df = pd.read_csv('data/processed_data.csv')
df.sort_values(by=['id', 'year'], inplace=True)

df_A = filter_A(df)

fig_A = px.line(df_A, x='year', y='percent_participation', color='progress_names',
                line_dash='goal_names', hover_data=['camp_name', 'location'], line_group='id')

fig_A.update_layout(
    autosize=False,  # Disable autosize
    width=1600,  # Set figure width
    height=1000,  # Set figure height
    xaxis_title='Year',
    yaxis_title='Campaign Size',
    title='Campaign Sizes over Time',
    xaxis={'fixedrange': True},  # Disable dragging on x-axis
    yaxis={'type': 'log', 'fixedrange': True, 'range': [0, np.log10(80)]}  # Use log scale and disable dragging on y-axis,
)

fig_A.update_traces(showlegend=False, line=dict(width=3))


color_trace = px.line(
    df_A,
    x="year",
    y=np.full(len(df_A), -1000),
    color="progress_names",
).update_traces(legendgrouptitle_text="Progress", legendgroup=str("Legends"))

linetype_trace = px.line(
    df_A,
    x="year",
    y=np.full(len(df_A), -1000),
    line_dash="goal_names",
).update_traces(legendgrouptitle_text="Goals", legendgroup=str(" "), line_color='white')


fig_A.add_traces(color_trace.data)
fig_A.add_traces(linetype_trace.data)


import plotly.express as px

# Filter the DataFrame based on the campaign goal
df_CD = filter_CD(df)  # Replace 'Your Campaign Goal' with your filter

# Create a temporary 'count' column to use for the pie chart values
df_CD['count'] = 1

# Create a pie chart for each combination of state reaction and violence level
fig_CD = px.pie(df_CD, values='count', names='success',
             facet_col='repression', facet_row='prim_meth',
             color='success',
             color_discrete_map={'Success':'green', 'Failure':'red'})

# Customize the layout
fig_CD.update_layout(
    autosize=False,
    width=800,
    height=500,
    title_text="Violence and State Reaction Analysis"
)



st.title('Behaviour of Protests Across The Globe and Their Outcome ')
st.write('''
# Explanation of the Plot
Here we show the size of different campaigns over time. 
The different line styles represent different campaign goals, 
while the colors (which are hidden in the legend) represent different progress names. 
You can hover over the lines to see more detailed information for each data point.
''')
st.plotly_chart(fig_A)
st.plotly_chart(fig_CD)

# appointment = st.slider(
#     "Schedule your appointment:",
#     value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)
