import streamlit as st
st.set_page_config(layout="wide")


def page1():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import streamlit as st
    import os


    os.chdir(r"C:\Users\Lior\Desktop\Information-Visualization")
    from Filters.Filters import filter_CD, filter_E, filter_F

    if st.button("Campaign Size and Success"):
        st.session_state.page = page2

    df = pd.read_csv('data/processed_data.csv')
    df.sort_values(by=['id', 'year'], inplace=True)

    df_F = filter_F(df)
    df_F['progress_names'] = df_F['progress_names'].str.title()
    df_F['goal_names'] = df_F['goal_names'].str.title()

    df_F['progress_names'] = df_F['progress_names'].replace({'ends in failure': 'Failed Immediately'})
    df_F = df_F.groupby(['goal_names', 'progress_names']).size().reset_index(name='counts')
    df_F['percent'] = df_F.groupby(['goal_names'])['counts'].transform(lambda x: x / x.sum() * 100)
    df_F['percent_str'] = df_F['percent'].round(2).astype(str) + '%'

    # Create a bar plot faceted by goal and x axis
    fig_F = px.bar(df_F, x="progress_names", y="percent", facet_col="goal_names",
                   color="progress_names",
                   color_discrete_sequence=px.colors.sequential.YlGn,
                   color_discrete_map={"Failed Immediately".title(): "salmon",
                                       "status quo".title(): "#ffffe5",
                                       "limited concession achieved".title(): "#d9f0a3",
                                       "visible gains short of concessions".title(): "#addd8e",
                                       "significant concessions achieved".title(): "#41ab5d",
                                       "complete success".title(): "#006837"},
                   category_orders={"progress_names": ["Failed Immediately",
                                                       "status quo".title(),
                                                       "limited concession achieved".title(),
                                                       "visible gains short of concessions".title(),
                                                       "significant concessions achieved".title(),
                                                       "complete success".title()]},
                   labels={"progress_names": "Best Achievement in Campaign"},
                   text="percent_str",
                   facet_col_wrap=2, height=600, width=1100,
                   )

    # limit y axis to 0-40
    fig_F.update_layout(
        coloraxis={"colorscale": px.colors.sequential.Darkmint},
        yaxis=dict(range=[0, 40]),
        legend=dict(
            orientation="h",
            yanchor="bottom",

            y=-0.15  # change this value to move the legend lower

            # xanchor="left",
        ))

    # remove progress names from x axis but keep the pacet titles
    fig_F.update_xaxes(title_text='')
    fig_F.update_xaxes(showticklabels=False)
    fig_F.update_xaxes(showgrid=False)

    for a in fig_F.layout.annotations:
        a.text = a.text.split("=")[1]
        # increase font size
        a.font.size = 18

    fig_F.update_layout(

        yaxis_title='Percent of Total',
        xaxis={'fixedrange': True},  # Disable dragging on x-axis
        yaxis={'fixedrange': True, 'range': [0, 45]},  # Use log scale and disable dragging on y-axis,
    )

    st.title('Campaign Goal Comparison')
    st.write('''
    This is a bar plot displaying the distribution of progress for each campaign goal. The x axis is the best progress achieved, and the y axis is the percent of campaigns that fall into that progress category. The color of the bars represents the progress category. The facet columns represent the campaign goal.

    Please note that all the campaigns that don't have "complete success" as a progress category have ended in failure, but we chose the best status achieved for the campaigns.
    ''')
    st.plotly_chart(fig_F)

    # Filter the DataFrame based on the campaign goal
    CD_res = filter_CD(df)  # Replace 'Your Campaign Goal' with your filter
    if CD_res[2]:
        CD_dfs = [CD_res[0], CD_res[1]]
    else:
        CD_dfs = [CD_res[0]]

    # Create a temporary 'count' column to use for the pie chart values

    # Create a pie chart for each combination of state reaction and violence level
    figs_CD = []
    if len(CD_dfs) == 1:
        titles = ['']
    else:
        titles = ['Regime Change', 'Greater Autonomy']
    for i, df_CD in enumerate(CD_dfs):

        fig_CD = px.pie(df_CD, values='count', names='success',
                        facet_col='repression_names', facet_row='resistance method',
                        color='success',
                        color_discrete_map={'Success': '#00FF7F', 'Failure': 'salmon'},
                        title=titles[i],
                        category_orders={
                            "repression_names": ["extreme repression", "moderate repression", "mild repression",
                                                 "none"],
                            "resistance method": ["never violent", "sometimes violent", "always violent"]})

        for a in fig_CD.layout.annotations:
            a.text = a.text.split("=")[1]

        # Customize the layout
        fig_CD.update_layout(
            autosize=False,
            width=750,
            height=500,
            title_text=titles[i],
            title_x=0.5,
        )
        if len(CD_dfs) == 2 and i == 0:
            fig_CD.update_layout(
                showlegend=False
            )

        for a in fig_CD['layout']['annotations']:
            if a['text'] in ["always violent", "never violent", "sometimes violent"]:
                a["textangle"] = 50
                a["xref"] = "paper"
                a["yref"] = "paper"
                a["x"] -= 0.04
                # a["y"] = 1 - (i / 2)

                a['align'] = "left"
                # incrase font size
            else:
                a['y'] = a['y'] + 0.05
            if a['text'] == 'none':
                a['text'] = 'No Repression'

            a['font'] = dict(size=15)
            if i == 0 and a['text'] in ["always violent", "never violent", "sometimes violent"]:
                a['font'] = dict(size=1, color='black')
            a['text'] = a['text'].title()
        figs_CD.append(fig_CD)

    df_E = filter_E(df)
    # Combine goal, intervention, and progress to create unique nodes
    df_E['goal_intervention'] = df_E['goal_names'] + '_' + df_E['ab_internat']
    df_E['intervention_progress'] = df_E['ab_internat'] + '_' + df_E['progress_names']

    # Create unique mappings for your categories
    goal_intervention_mapping = {goal_intervention: i for i, goal_intervention in
                                 enumerate(df_E['goal_intervention'].unique())}
    intervention_progress_mapping = {intervention_progress: i + len(goal_intervention_mapping) for
                                     i, intervention_progress in enumerate(df_E['intervention_progress'].unique())}

    # Apply the mappings to your columns
    df_E['goal_intervention_codes'] = df_E['goal_intervention'].map(goal_intervention_mapping)
    df_E['intervention_progress_codes'] = df_E['intervention_progress'].map(intervention_progress_mapping)

    # Rest of the code...

    progress_order = ['Complete Success', 'Significant Concessions Achieved', 'Limited Concession Achieved',
                      'Visible Gains Short Of Concessions', 'Status Quo', 'Ends In Failure']
    # Iterate over each goal
    df_E = filter_E(df)
    df_E['progress_names'] = df_E['progress_names'].str.title()
    # Combine goal, intervention, and progress to create unique nodes
    # df_E['goal_intervention'] = df_E['goal_names'] + '_' + df_E['ab_internat']
    df_E['intervention_progress'] = df_E['ab_internat'] + '_' + df_E['progress_names']

    # Create unique mappings for your categories
    # goal_intervention_mapping = {goal_intervention: i for i, goal_intervention in enumerate(df_E['goal_intervention'].unique())}
    intervention_progress_mapping = {intervention_progress: i + len(goal_intervention_mapping) for
                                     i, intervention_progress in enumerate(df_E['intervention_progress'].unique())}

    # Apply the mappings to your columns
    # df_E['goal_intervention_codes'] = df_E['goal_intervention'].map(goal_intervention_mapping)
    df_E['intervention_progress_codes'] = df_E['intervention_progress'].map(intervention_progress_mapping)

    # Rest of the code...
    # Iterate over each goal
    E_figs = []
    color_dict = {
        'No Intervention': '#FFA07A',
        'Material Reprucussions': '#4682B4',
        'Complete Success': '#006400',  # Darker green
        'Limited Concession Achieved': '#A2CD5A',  # Darker yellowgreen
        'Status Quo': 'orange',  # Gold
        'Significant Concessions Achieved': '#6E8B3D',  # Lighter yellowgreen
        'Ends In Failure': '#8B0000',  # Dark red
        'Visible Gains Short Of Concessions': '#FFD700',  # YellowGreen
        'Greater Autonomy': '#808080'  # Gray
    }
    for goal, df_goal in df_E.groupby('goal_names'):
        # Create unique mappings for your categories
        intervention_mapping = {name: i for i, name in enumerate(df_goal['ab_internat'].unique())}
        progress_mapping = {name: i + len(intervention_mapping) for i, name in
                            enumerate(df_goal['progress_names'].unique())}

        # Apply the mappings to your columns
        df_goal['intervention_codes'] = df_goal['ab_internat'].map(intervention_mapping)
        df_goal['progress_codes'] = df_goal['progress_names'].map(progress_mapping)

        # Create source, target and value lists
        source = df_goal['intervention_codes'].tolist()
        target = df_goal['progress_codes'].tolist()
        values = [1 for _ in range(len(source))]
        sankey_data = pd.DataFrame({'source': source, 'target': target, 'values': values}).sort_values(
            ['source', 'target'])
        # Create colors for each source node
        colors = df_goal['intervention_codes'].map(
            {code: color for code, color in enumerate(['#4682B4', '#FFA07A'])}).tolist()
        node_positions = {
            'Material Reprucussions': [0.001, 0.001],
            'No Intervention': [0.001, 0.7],
            'Complete Success': [0.999, 0.001],
            'Significant Concessions Achieved': [0.999, 0.2],
            'Limited Concession Achieved': [0.999, 0.4],
            'Visible Gains Short Of Concessions': [0.999, 0.6],
            'Status Quo': [0.999, 0.8],
            'Ends In Failure': [.999, .999]
        }
        # Create the label list with counts included
        label_counts = df_goal['ab_internat'].value_counts().to_dict()
        label = [f'{name} ({label_counts[name]})' if name in label_counts else name for name in
                 list(intervention_mapping.keys()) + list(progress_mapping.keys())]
        # Create a list of all unique nodes in the correct order
        # all_nodes_E = df_goal['goal_names'].unique().tolist() + df_goal['ab_internat'].unique().tolist()

        # Add progress nodes in the correct order
        all_nodes_E = df_goal['ab_internat'].unique().tolist() + df_goal['progress_names'].unique().tolist()

        # Manually order the labels based on desired_order
        ordered_labels = [label for label in all_nodes_E if label not in progress_order] + [label for label in
                                                                                            progress_order if
                                                                                            label in all_nodes_E]
        # Create a Sankey plot
        fig_E = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=ordered_labels,
                color=[color_dict.get(node, '#808080') for node in ordered_labels],
                x=[node_positions.get(node, [0.01, 0.01])[0] for node in ordered_labels],
                y=[node_positions.get(node, [0.01, 0.01])[1] for node in ordered_labels]
            ),
            link=dict(
                source=source,
                target=target,
                value=values,
                color=colors,  # Add the colors
            )
        )])

        # Display the plot

        # Set the layout options
        fig_E.update_layout(title_text=f'{str(goal).title()}', font_size=14, height=500, width=600, title_y=1,
                            autosize=True, margin=dict(l=50, r=50, b=100, t=100, pad=4))
        E_figs.append(fig_E)

    st.title('Violence and State Reaction Analysis')
    st.write('''
    This histogram shows the the success rate of campaigns based on the percentage of the population involved in the campaign.
    ''')
    if len(figs_CD) == 1:
        st.plotly_chart(figs_CD[0])
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(figs_CD[0])
        with col2:
            st.plotly_chart(figs_CD[1])

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


def page2():
    # %%
    import pandas as pd
    import os
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    import streamlit as st
    import sys
    if st.button("Campaign Goal Comparison"):
        st.session_state['page'] = page1
    os.chdir(r"C:\Users\Lior\Desktop\Information-Visualization")
    print(os.getcwd())

    df = pd.read_csv('data/processed_data.csv')
    df.sort_values(by=['id', 'year'], inplace=True)
    #
    st.title('Campaign By Sizes and their Achievements Over Time')
    st.write('''
    Here we show the size of different campaigns over time.
    The width represents the Relative size of the campaign compared to the population of the country in a specific year (in percents).
    The the colors represent the Achievements for that Year
    You can hover over the lines to see more detailed information for each data point.
    ''')
    from Filters.Filters import filter_A

    df_A, ids = filter_A(df)

    A_color_dict = {
        'complete success': '#006400',  # Darker green
        'visible gains short of concessions': '#FFD700',  # YellowGreen
        'limited concession achieved': '#A2CD5A',  # Darker yellowgreen
        'status quo': 'orange',  # Gold
        'significant concessions achieved': '#6E8B3D',  # Lighter yellowgreen
        'ends in failure': '#8B0000',  # Dark red
    }

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

    # translate df_A['progress_names'] to colors

    df_A['color'] = df_A['progress_names'].apply(lambda x: color_dict[x])

    # df_A["line_width"]  = df_A["line_width"].apply(lambda x: int(x))

    # fig_A = px.line(df_A, x='year', y='percent_participation', color='progress_names',
    #                 line_dash='goal_names', hover_data=['camp_name', 'location'], line_group='id')

    # goals_to_type = {"greater autonomy": "dash", "regime change": "solid"}

    colors = list(A_color_dict.values())
    progresses = list(A_color_dict.keys())

    fig_A = go.Figure()

    # Create a trace for each color and progress
    def width_bracket(percent):
        if percent < 0.1:
            width = 1
        elif percent < 0.25:
            width = 2
        elif percent < 0.5:
            width = 3
        elif percent < 1:
            width = 4
        elif percent < 1.5:
            width = 5
        elif percent < 2:
            width = 6
        elif percent < 5:
            width = 7
        elif percent < 10:
            width = 8
        else:
            width = 9
        return width

    campaign_names = []
    for i, id in enumerate(ids):
        df_temp = df_A[df_A['id'] == id]
        campaign_names.append(df_temp['camp_name'].iloc[0])
        unique_years = df_temp['year'].unique()
        ## add another year that is 1 year after the last year and has the same values
        unique_years = np.append(unique_years, unique_years[-1] + 1)

        latest_year_row = df_temp[df_temp['year'] == df_temp['year'].max()]

        new_row = latest_year_row.copy()
        new_row['year'] = new_row['year'] + 1
        df_temp = df_temp.append(new_row, ignore_index=True)

        for year in unique_years:
            df_years = df_temp[(df_temp['year'] == year) | (df_temp['year'] == year + 1)]

            # width = np.clip(np.log2(float(abs(df_years["percent_participation"].iloc[0]))*1000 + 0.0001), 0.05, 10)
            width = width_bracket(df_years["percent_participation"].iloc[0]) * 2

            if np.isnan(width):
                width = 0

            fig_A.add_trace(go.Scatter(
                x=df_years['year'],
                y=[i] * len(df_years),
                mode='lines',
                marker=dict(color=df_years['color'].iloc[0]),
                line=dict(color="lightslategray", width=width + 1.5),
                customdata=list(zip(df_years['id'], df_years['progress_names'], df_years['percent_participation'],
                                    df_years['camp_name'])),
                # Use a list of tuples containing the id and progress names
                hovertemplate='Campaign ID: %{customdata[0]}<br>Year: %{x}<br>Progress: %{customdata[1]} <br> Relative Size: %{customdata[2]} <br> Campaign Name: %{customdata[3]}'
                # Use the first values of the custom data columns
            ))

            fig_A.add_trace(go.Scatter(
                x=df_years['year'],
                y=[i] * len(df_years),
                mode='lines',
                marker=dict(color=df_years['color'].iloc[0]),
                line=dict(color=df_years['color'].iloc[0], width=width),
                customdata=list(zip(df_years['id'], df_years['progress_names'], df_years['percent_participation'],
                                    df_years['camp_name'])),
                # Use a list of tuples containing the id and progress names
                hovertemplate='Campaign ID: %{customdata[0]}<br>Year: %{x}<br>Progress: %{customdata[1]} <br> Relative Size: %{customdata[2]} <br> Campaign Name: %{customdata[3]}'
                # Use the first values of the custom data columns
            ))

    years_range = int((df_A['year'].max() - df_A['year'].min()) // 2)
    years_grid = list(range(df_A['year'].min(), df_A['year'].max(), 2))
    max_val = df_A['percent_participation'].max()
    fig_A.update_layout(
        autosize=False,  # Disable autosize
        width=1100,  # Set figure width
        height=790,  # Set figure height
        xaxis_title='Year',
        yaxis_title='Campaign Name',
        xaxis={'fixedrange': True},  # Disable dragging on x-axis
        yaxis={'fixedrange': True, 'range': [0, len(ids)],
               'tickvals': list(range(len(ids))),  # Set tick values to the index of each campaign
               'ticktext': campaign_names, 'showgrid': True  # Set tick labels to the names of the campaigns
               },  # Use log scale and disable dragging on y-axis,

    )

    fig_A.update_traces(showlegend=False)

    progress_order = [
        'ends in failure',
        'status quo',
        'visible gains short of concessions',
        'limited concession achieved',
        'significant concessions achieved',
        'complete success'
    ]
    progress_order.reverse()

    color_trace = px.line(
        df_A,
        x="year",
        y=np.full(len(df_A), -1000),
        color="progress_names",
        color_discrete_map=color_dict,  # Use the color_dict as the color map
        category_orders={"progress_names": progress_order}  # Use the progress_order as the category order
    ).update_traces(legendgrouptitle_text="Campaign Progress", legendgroup=str("Legends"))

    fig_A.add_traces(color_trace.data)

    # Create a dummy trace for the width legend
    width_trace = go.Scatter(
        x=[df_A['year'].min()],  # Use the minimum year as the x value
        y=[-1000],  # Use the same dummy y value as the color trace
        mode='markers',  # Use markers instead of lines
        marker=dict(color='white', size=10, symbol='triangle-left'),
        # Use a triangle symbol with a constant size and color
        name='width = Relative Campaign Size',  # Use the desired legend text
        showlegend=True  # Show this trace in the legend
    )

    fig_A.add_trace(width_trace)

    st.plotly_chart(fig_A)

    # st.title('Campaign Size Distribution')
    st.title('Campaign Size Effect on Success Rate')
    st.write('''
    This histogram shows Chances of success by Campaign Size (Relative to Country Population).
    ''')
    from Filters.filter_B import filter_B

    df_B2, df_B1, num_bins = filter_B(df, 'Small')
    # Define the number of bins and bin width
    bin_width = (df_B1['stat'].max() - df_B1['stat'].min()) / num_bins

    # Create the bins
    bins = np.arange(0, df_B1['stat'].max(), bin_width)

    # Group the data into the bins and calculate the average success percentage
    df_B1['stat_bins'] = pd.cut(df_B1['stat'], bins)
    grouped = df_B1.groupby('stat_bins')['success'].mean()

    # Convert Interval object to string representation
    x_values = [str(interval) for interval in grouped.index]

    # Get the count of data points in each bin
    counts = df_B1['stat_bins'].value_counts().reindex(grouped.index, fill_value=0)

    # Create the hovertemplate
    hovertemplate = (
        "Bin: %{x}<br>"
        "Success Percentage: %{y:.2f}%<br>"
        "Data Points: %{customdata}"
    )

    success_percentage = grouped * 100
    rounded_percentage = round(success_percentage, 2)

    # Create the bar trace with the desired color and rounded values
    trace = go.Bar(
        x=x_values,
        y=grouped * 100,  # Multiply by 100 to get percentage
        marker=dict(color='rgb(128, 177, 211)'),
        text=rounded_percentage,
        customdata=counts,
        texttemplate='%{text:.0f}%',  # Format the text as rounded percentage with 2 decimal places
        hovertemplate=hovertemplate,
        hovertext=counts,  # Set the hover text to the counts
    )

    # Create the layout
    layout = go.Layout(
        title='Small Campaigns (Up to 1.5%)',
        xaxis=dict(title='Percent of Population Present In Campaign'),
        yaxis=dict(title='Success Percentage')
    )

    # Create the figure
    fig_B1 = go.Figure(data=[trace], layout=layout)

    bin_width = (df_B2['stat'].max() - df_B2['stat'].min()) / num_bins

    # Create the bins
    bins = np.arange(1.5, df_B2['stat'].max() + bin_width, bin_width)

    # Group the data into the bins and calculate the average success percentage
    df_B2['stat_bins'] = pd.cut(df_B2['stat'], bins)
    grouped = df_B2.groupby('stat_bins')['success'].mean()

    # Convert Interval object to string representation
    x_values = [str(interval) for interval in grouped.index]

    # Get the count of data points in each bin
    counts = df_B2['stat_bins'].value_counts().reindex(grouped.index, fill_value=0)

    # Create the hovertemplate
    hovertemplate = (
        "Bin: %{x}<br>"
        "Success Percentage: %{y:.2f}%<br>"
        "Data Points: %{customdata}"
    )

    success_percentage = grouped * 100
    rounded_percentage = round(success_percentage, 2)

    # Create the bar trace with the desired color and rounded values
    trace = go.Bar(
        x=x_values,
        y=grouped * 100,  # Multiply by 100 to get percentage
        marker=dict(color='rgb(128, 177, 211)'),
        text=rounded_percentage,
        customdata=counts,
        texttemplate='%{text:.0f}%',  # Format the text as rounded percentage with 2 decimal places
        hovertemplate=hovertemplate,
        hovertext=counts,  # Set the hover text to the counts
    )

    # Create the layout
    layout = go.Layout(
        title='Large Campaigns (Larger than 1.5%)',
        xaxis=dict(title='Percent of Population Present In Campaign'),
        yaxis=dict(title='Success Percentage')
    )

    # Create the figure
    fig_B2 = go.Figure(data=[trace], layout=layout)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_B1)
    with col2:
        st.plotly_chart(fig_B2)


if 'page' not in st.session_state:
    st.session_state['page'] = page1
else:
    print(st.session_state['page'])

# Use radio buttons for navigation
# page = st.radio("Choose a page", tuple(pages.keys()))
st.session_state['page']()
# Display the selected page with the session state
