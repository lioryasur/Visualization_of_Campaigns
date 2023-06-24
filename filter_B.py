
import pandas as pd
import streamlit as st


def calculate_stat(df, stat_choice):
    result = {}
    if stat_choice == 'Average':
        result['stat'] = df['percent_participation'].mean()
    elif stat_choice == 'Max':
        result['stat'] = df['percent_participation'].max()
    elif stat_choice == 'Sum':
        result['stat'] = df['percent_participation'].sum()
    elif stat_choice == 'Last Year':
        result['stat'] = df.loc[df['year'].idxmax()]['percent_participation']

    result['success'] = df.loc[df['year'].idxmax()]['success']
    return pd.Series(result)

def filter_B(df: pd.DataFrame, campaign_type):
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """

    df = df.copy()

    #campaign_type = st.selectbox("Large or Small Campaigns (by percent of populations)", ['Large', 'Small'], index=1)



    df = df[df['population_bad'] == False]


    modification_container = st.container()

    with modification_container:
        stat_choice = st.selectbox("Choose Statistic for Calculating Participation",['Average', 'Max', 'Sum', 'Last Year'])
        df = df.groupby('id').apply(calculate_stat, stat_choice=stat_choice).reset_index()  # Replace 'avg' with your actual choice
        df.columns = ['id', 'stat', 'success']

    df = df[df['stat'] < 15]
    df_large = df[df['stat'] > 2]
    df_small = df[df['stat'] <= 2]

    n_bins = st.selectbox("Number of bins", [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], index=4)

    return df_large, df_small, n_bins
# Define the user's choice for the statistic
