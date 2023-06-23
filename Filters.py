
import pandas as pd
import streamlit as st

# def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Adds a UI on top of a dataframe to let viewers filter columns
#
#     Args:
#         df (pd.DataFrame): Original dataframe
#
#     Returns:
#         pd.DataFrame: Filtered dataframe
#     """
#     modify = st.checkbox("Add filters")
#
#     if not modify:
#         return df
#
#     df = df.copy()
#
#     # Try to convert datetimes into a standard format (datetime, no timezone)
#     for col in df.columns:
#         if is_object_dtype(df[col]):
#             try:
#                 df[col] = pd.to_datetime(df[col])
#             except Exception:
#                 pass
#
#         if is_datetime64_any_dtype(df[col]):
#             df[col] = df[col].dt.tz_localize(None)
#
#     modification_container = st.container()
#
#     with modification_container:
#         to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
#         for column in to_filter_columns:
#             left, right = st.columns((1, 20))
#             # Treat columns with < 10 unique values as categorical
#             if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
#                 user_cat_input = right.multiselect(
#                     f"Values for {column}",
#                     df[column].unique(),
#                     default=list(df[column].unique()),
#                 )
#                 df = df[df[column].isin(user_cat_input)]
#             elif is_numeric_dtype(df[column]):
#                 _min = float(df[column].min())
#                 _max = float(df[column].max())
#                 step = (_max - _min) / 100
#                 user_num_input = right.slider(
#                     f"Values for {column}",
#                     min_value=_min,
#                     max_value=_max,
#                     value=(_min, _max),
#                     step=step,
#                 )
#                 df = df[df[column].between(*user_num_input)]
#             elif is_datetime64_any_dtype(df[column]):
#                 user_date_input = right.date_input(
#                     f"Values for {column}",
#                     value=(
#                         df[column].min(),
#                         df[column].max(),
#                     ),
#                 )
#                 if len(user_date_input) == 2:
#                     user_date_input = tuple(map(pd.to_datetime, user_date_input))
#                     start_date, end_date = user_date_input
#                     df = df.loc[df[column].between(start_date, end_date)]
#             else:
#                 user_text_input = right.text_input(
#                     f"Substring or regex in {column}",
#                 )
#                 if user_text_input:
#                     df = df[df[column].astype(str).str.contains(user_text_input)]
#
#     return df

def filter_A(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df
    df = df[df['population_bad'] == False]
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", ['Year', 'Goal'])
        # ['year', 'campaign_goal']
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if column == 'Goal':
                column = 'goal_names'
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif column == 'Year':
                column = 'year'
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
    return df


def calculate_stat(df, stat_choice):
    result = {}
    if stat_choice == 'avg':
        result['stat'] = df['percent_participation'].mean()
    elif stat_choice == 'max':
        result['stat'] = df['percent_participation'].max()
    elif stat_choice == 'sum':
        result['stat'] = df['percent_participation'].sum()
    elif stat_choice == 'last':
        result['stat'] = df.loc[df['year'].idxmax()]['percent_participation']

    result['success'] = df.loc[df['year'].idxmax()]['success']
    return pd.Series(result)


def filter_B(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Choose statistic")
    df = df[df['population_bad'] == False]
    if not modify:
        df = df.groupby('id').apply(calculate_stat, stat_choice='avg').reset_index()  # Replace 'avg' with your actual choice
        #print(df.columns)
        #df = df.reset_index()
        df.columns = ['id', 'stat', 'success']
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        stat_choice = st.selectbox("Choose Statistic",['Average', 'Max', 'Sum', 'Last'])
        df_B = df.groupby('id').apply(calculate_stat, stat_choice=stat_choice).reset_index()  # Replace 'avg' with your actual choice
        df = df.reset_index()
        df.columns = ['id', 'stat', 'success']

    return df
# Define the user's choice for the statistic
stat_choice = 'avg'  # Change this to 'avg', 'max', 'sum', or 'last' based on the user's choice


def filter_CD(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """

    success_values = {0: 'Failure', 1: 'Success'}
    df['success'] = df['success'].map(success_values)
    df = df[df["repression_names"] != "unknown"]

    modify = st.checkbox("CD Filters")

    if not modify:
        return df

    df = df.copy()


    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on",['Goal'])
        # ['year', 'campaign_goal']
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if column == 'Goal':
                column = 'goal_names'
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
    return df