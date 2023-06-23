
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
        left, right = st.columns((1, 20))

        column = 'year'
        _min = float(df[column].min())
        _max = float(df[column].max())
        step = (_max - _min) / 100
        user_num_input = right.slider(
            f"Values for {column}",
            min_value=float(_min),
            max_value=float(_max),
            value=(float(1983), float(1993)),  # Set the default range
            step=float(step),
        )
        df = df[df[column].between(*user_num_input)]
        df.sort_values(by=['year'], inplace=True)
        cy0id = df[df["cyear"] == 0]["id"]
        cy1id = df[df["cyear"] == 1]["id"]

        ids = set(cy0id).intersection(set(cy1id))
        df = df[df["id"].isin(ids)]

        return df, df["id"].unique()

    df = df[df['percent_participation'] < 12]
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
                    min_value=float(_min),
                    max_value=float(_max),
                    value=(float(1983), float(1993)),  # Set the default range
                    step=float(step),
                )
                df = df[df[column].between(*user_num_input)]
                df.sort_values(by=['year'], inplace=True)
                cy0id = df[df["cyear"] == 0]["id"]
                cy1id = df[df["cyear"] == 1]["id"]

                ids = set(cy0id).intersection(set(cy1id))
                df = df[df["id"].isin(ids)]

    return df, df["id"].unique()


def calculate_stat(df, stat_choice):
    result = {}
    if stat_choice == 'Average':
        result['stat'] = df['percent_participation'].mean()
    elif stat_choice == 'Max':
        result['stat'] = df['percent_participation'].max()
    elif stat_choice == 'Sum':
        result['stat'] = df['percent_participation'].sum()
    elif stat_choice == 'Last':
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
    modify = st.checkbox("Choose statistic for calculating percent participation of campaign across its years")



    df = df.copy()

    campaign_type = st.selectbox("Large or Small Campaigns (by percent of populations)", ['Large', 'Small'], index=1)



    df = df[df['population_bad'] == False]

    if not modify:
        df_new = df.groupby('id').apply(calculate_stat, stat_choice='Average').reset_index()  # Replace 'avg' with your actual choice
        df_new.columns = ['id', 'stat', 'success']

        df_new = df_new[df_new['stat'] < 15]
        if campaign_type == 'Large':
            df_new = df_new[df_new['stat'] > 2]
        else:
            df_new = df_new[df_new['stat'] < 2]

        return df_new



    modification_container = st.container()

    with modification_container:
        stat_choice = st.selectbox("Choose Statistic",['Average', 'Max', 'Sum', 'Last'])
        df = df.groupby('id').apply(calculate_stat, stat_choice=stat_choice).reset_index()  # Replace 'avg' with your actual choice
        print(df)
        df.columns = ['id', 'stat', 'success']

    df = df[df['stat'] < 15]
    if campaign_type == 'Large':
        df = df[df['stat'] > 2]
    else:
        df = df[df['stat'] < 2]

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

def filter_E(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """

    df = df.copy()
    progress_values = {0: "status quo", 1: "visible gains short of concessions", 2: "limited concession achieved",
                       3: "significant concessions achieved", 4: "complete success", -1: "ends in failure",
                       -99: "unknown"}

    df = df[df['ab_internat'] != -99]
    new_df = {'goal_names': [], 'ab_internat': [], 'progress_names': []}
    for id in df['id'].unique():
        cur_df = df[df['id'] == id]
        max_progress = cur_df['progress'].max()
        new_df['progress_names'].append(progress_values[max_progress])
        new_df['goal_names'].append(cur_df['goal_names'].iloc[0])
        if 1 in cur_df['ab_internat'].unique():
            new_df['ab_internat'].append('Material Reprucussions')
        else:
            new_df['ab_internat'].append('No Intervention')

    return pd.DataFrame(new_df)