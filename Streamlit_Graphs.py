# %%
import dash
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
from Filters import filter_A, filter_B, filter_CD

os.chdir(r"C:\Users\Freddie\Desktop\personal\Information-Visualization")

df = pd.read_csv('data/processed_data.csv')
df.sort_values(by=['id', 'year'], inplace=True)

df_A = filter_A(df)

fig_A = px.line(df_A, x='year', y='percent_participation', color='progress_names',
                line_dash='goal_names', hover_data=['camp_name', 'location'], line_group='id')

fig_A.update_layout(
    autosize=False,  # Disable autosize
    width=1000,  # Set figure width
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


df_B = filter_B(df)  # Apply your filter function to the DataFrame, replace filter_B(df) with your actual function
num_data_points_per_bin = 20
df_B = df_B.sort_values(by='stat')
# Create the histogram
bin_edges = np.array([0, 0.25, 0.5, 0.75, 1, 1.50, 2, 2.5, 3, 4, 100])

# fig_B = px.histogram(df_B, x='stat', color='success', nbins=10)
#
# fig_B.update_layout(
#     autosize=False,
#     width=800,
#     height=500,
#     title_text="Campaign Size Distribution",
#     barmode='stack'
# )



# Define colors for success values
success_colors = {1: 'green', 0: 'red'}

# Create a list to store the bar traces
bar_traces = []

# Iterate over the success values
for success in success_colors.keys():
    # Filter the counts based on success value
    relevant = df_B[df_B['success'] == success]
    counts, edges = np.histogram(relevant.stat, bins=bin_edges)
    centers = 0.5 * (edges[:-1] + edges[1:])
    widths = edges[1:] - edges[:-1]
    # Create a bar trace with custom widths
    bar_trace = go.Bar(
        x=centers,
        y=counts,
        width=0.25,
        name=success,
        marker_color=success_colors[success]
    )

    # Append the bar trace to the list
    bar_traces.append(bar_trace)

# Create the figure with stacked bar traces
fig_B = go.Figure(data=bar_traces)

fig_B.update_layout(
    autosize=False,
    width=800,
    height=500,
    title_text="Campaign Size Distribution",
    xaxis_title="Stat",
    yaxis_title="Count",
    barmode='stack',
    xaxis_type='log'
)

st.title('Campaign Size Distribution')
st.write('''
# Explanation of the Plot
This histogram shows the distribution of campaign sizes. The bars are split in the middle by color based on the success values.
''')
st.plotly_chart(fig_B)



# Filter the DataFrame based on the campaign goal
df_CD = filter_CD(df)  # Replace 'Your Campaign Goal' with your filter

# Create a temporary 'count' column to use for the pie chart values
df_CD['count'] = 1

# Create a pie chart for each combination of state reaction and violence level
fig_CD = px.pie(df_CD, values='count', names='success',
             facet_col='repression_names', facet_row='resistance method',
             color='success',
             color_discrete_map={'Success':'#00FF7F', 'Failure':'salmon'},
            title='Violence and State Reaction Analysis',
        category_orders={"repression_names": ["extreme repression", "moderate repression", "mild repression", "none"],
                         "resistance": ["always violent", "never violent", "sometimes violent"]})






for a in fig_CD.layout.annotations:
    a.text = a.text.split("=")[1]

# Customize the layout
fig_CD.update_layout(
    autosize=False,
    width=800,
    height=500,
    title_text="Violence and State Reaction Analysis",
)

for i, a in enumerate(fig_CD['layout']['annotations']):
    if a['text'] in  ["always violent", "never violent", "sometimes violent"]:
        a["textangle"] = 50
        a["xref"] = "paper"
        a["yref"] = "paper"
        # a["x"] = 0.02
        # a["y"] = 1 - (i / 2)
        a['align'] = "left"
        #incrase font size
    a['font'] = dict(size=15)





st.title('Behaviour of Protests Across The Globe and Their Outcome ')
st.write('''
# Explanation of the Plot
Here we show the size of different campaigns over time. 
The different line styles represent different campaign goals, 
while the colors (which are hidden in the legend) represent different progress names. 
You can hover over the lines to see more detailed information for each data point.
''')
st.plotly_chart(fig_A)



st.title('Campaign Size Distribution')
st.write('''
# Explanation of the Plot
This histogram shows the distribution of campaign sizes. The color indicates whether each campaign was successful or not.
''')
st.plotly_chart(fig_B)


st.plotly_chart(fig_CD)

# appointment = st.slider(
#     "Schedule your appointment:",
#     value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)
