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
from Filters import filter_A, filter_B, filter_CD, filter_E
import plotly.subplots as sp
os.chdir(r"C:\Users\Lior\Desktop\Information-Visualization")

df = pd.read_csv('data/processed_data.csv')
df.sort_values(by=['id', 'year'], inplace=True)

df_A, ids = filter_A(df)

color_dict = {
    'No Intervention': '#FFA07A',
    'Material Reprucussions': '#4682B4',
    'complete success': '#006400',  # Darker green
    'limited concession achieved': '#A2CD5A',  # Darker yellowgreen
    'status quo': 'orange',  # Gold
    'significant concessions achieved': '#6E8B3D',  # Lighter yellowgreen
    'ends in failure': '#8B0000',  # Dark red
    'visible gains short of concessions': '#FFD700',  # YellowGreen
    'greater autonomy': '#808080'  # Gray
}


#translate df_A['progress_names'] to colors

df_A['color'] = df_A['progress_names'].apply(lambda x: color_dict[x])

print(set(list(df_A['color'])))

# df_A["line_width"]  = df_A["line_width"].apply(lambda x: int(x))

# fig_A = px.line(df_A, x='year', y='percent_participation', color='progress_names',
#                 line_dash='goal_names', hover_data=['camp_name', 'location'], line_group='id')

# goals_to_type = {"greater autonomy": "dash", "regime change": "solid"}

figs_A = []
fig_A = go.Figure()
for i, id in enumerate(ids):
    df_temp = df_A[df_A['id'] == id]
    unique_years = df_temp['year'].unique()

    for year in unique_years:
        df_years = df_temp[(df_temp['year'] == year) | (df_temp['year'] == year + 1)]

        width = np.clip(np.log2(float(abs(df_years["percent_participation"].iloc[0]))*1000 + 0.0001), 0.05, 10)
        if np.isnan(width):
            width = 0

        fig_A.add_trace(go.Scatter(
            x=df_years['year'],
            y=[i]*len(df_years),
            mode='lines + markers',
            marker = dict(color = df_years['color'].iloc[0]),
            line=dict(color=df_years['color'].iloc[0], width=width)  # Assuming 'color' is a column in df_temp
        ))


max_val = df_A['percent_participation'].max()
fig_A.update_layout(
    autosize=False,  # Disable autosize
    width=1000,  # Set figure width
    height=810,  # Set figure height
    xaxis_title='Year',
    yaxis_title='Campign',
    title='Campaign Sizes over Time',
    xaxis={'fixedrange': True},  # Disable dragging on x-axis
    yaxis={ 'fixedrange': True, 'range': [0, len(ids)]},
    # Use log scale and disable dragging on y-axis,
)

fig_A.update_traces(showlegend=False)


color_trace = px.line(
    df_A,
    x="year",
    y=np.full(len(df_A), -1000),
    color="progress_names",
).update_traces(legendgrouptitle_text="progress_names", legendgroup=str("Legends"))


fig_A.add_traces(color_trace.data)


df_B = filter_B(df)

#Define the number of bins and bin width
num_bins = 10
bin_width = (df_B['stat'].max() - df_B['stat'].min()) / num_bins

#Create the bins
bins = np.arange(0, df_B['stat'].max() + bin_width, bin_width)

#Group the data into the bins and calculate the average success percentage
df_B['stat_bins'] = pd.cut(df_B['stat'], bins)
grouped = df_B.groupby('stat_bins')['success'].mean()

#Convert Interval object to string representation
x_values = [str(interval) for interval in grouped.index]

#Get the count of data points in each bin
counts = df_B['stat_bins'].value_counts().reindex(grouped.index, fill_value=0)

#Create the hovertemplate
hovertemplate = (
    "Bin: %{x}<br>"
    "Success Percentage: %{y:.2f}%<br>"
    "Data Points: %{customdata}"
)

success_percentage = grouped * 100
rounded_percentage = round(success_percentage, 2)

#Create the bar trace with the desired color and rounded values
trace = go.Bar(
    x=x_values,
    y=grouped * 100,  # Multiply by 100 to get percentage
    marker=dict(color='rgb(128, 177, 211)'),
    text=rounded_percentage,
    customdata = counts,
    texttemplate='%{text:.2f}%',  # Format the text as rounded percentage with 2 decimal places
    hovertemplate=hovertemplate,
    hovertext=counts,  # Set the hover text to the counts
)

#Create the layout
layout = go.Layout(
    title='Odds of Campaign Success by Portion of Population Involved',
    xaxis=dict(title='Percent of Population Present In Campaign'),
    yaxis=dict(title='Success Percentage')
)

#Create the figure
fig_B = go.Figure(data=[trace], layout=layout)

st.title('Campaign Size Distribution')
st.write('''
Explanation of the Plot
This histogram shows the distribution of campaign sizes. The bars are split in the middle by color based on the success values.
''')


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




df_E = filter_E(df)
# Combine goal, intervention, and progress to create unique nodes
df_E['goal_intervention'] = df_E['goal_names'] + '_' + df_E['ab_internat']
df_E['intervention_progress'] = df_E['ab_internat'] + '_' + df_E['progress_names']

# Create unique mappings for your categories
goal_intervention_mapping = {goal_intervention: i for i, goal_intervention in enumerate(df_E['goal_intervention'].unique())}
intervention_progress_mapping = {intervention_progress: i + len(goal_intervention_mapping) for i, intervention_progress in enumerate(df_E['intervention_progress'].unique())}

# Apply the mappings to your columns
df_E['goal_intervention_codes'] = df_E['goal_intervention'].map(goal_intervention_mapping)
df_E['intervention_progress_codes'] = df_E['intervention_progress'].map(intervention_progress_mapping)

# Rest of the code...


# Iterate over each goal
E_figs = []
for goal, df_goal in df_E.groupby('goal_names'):
    # Create the value counts for the links
    df_grouped_E = df_goal.groupby(['goal_intervention_codes', 'intervention_progress_codes']).size().reset_index(name='value')

    # Concatenate all nodes
    all_nodes_E = df_goal['goal_names'].unique().tolist() + df_goal['ab_internat'].unique().tolist() + df_goal['progress_names'].unique().tolist()

    # Create a Sankey plot
    fig_E = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=all_nodes_E,  # Make sure to update this as well to match the new nodes
        ),
        link=dict(
            source=df_grouped_E['goal_intervention_codes'],  # Use the new source column
            target=df_grouped_E['intervention_progress_codes'],  # Use the new target column
            value=df_grouped_E['value']
        )
    )])

    # Set the layout options
    fig_E.update_layout(title_text=f'International Intervention Analysis: {goal}', font_size=10)
    E_figs.append(fig_E)
    # Display the plot in Streamlit


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


st.title('International Intervention Analysis')
st.write('''
# Explanation of the Plot
This Sankey plot shows the relationship between international intervention and success in different types of campaigns. The plot is faceted by campaign goal, with each facet representing a different campaign goal. The first split is by international intervention, and each "tube" is further split by progress. The width of each tube represents the number of examples.
''')
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(E_figs[0])
with col2:
    st.plotly_chart(E_figs[1])

# appointment = st.slider(
#     "Schedule your appointment:",
#     value=(time(11, 30), time(12, 45)))
# st.write("You're scheduled for:", appointment)
