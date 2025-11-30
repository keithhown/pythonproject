import pandas as pd
import numpy as np
import ast

def load_and_clean_data(file_path):
    """
    load and clean the movies metadata dataset.
    parameters: 
        - file_path (str): path to the CSV file containing the dataset.
        - verbose (bool): if true prints first 5 rows of the dataset.
    returns: pd.DataFrame: cleaned and enriched dataframe ready for analysis with additional columns:
        - main_genre: primary genre inferred from genre list.
        - release_year: year of the movie release.
        - decade: Decade of release (e.g., 1990, 2000).
        - profit: revenue minus budget.
        - roi: return on investment (profit relative to budget).
        - runtime_category: classify movies based on their duration into three categories: short/standard/long.
        - is_profitable?: boolean flag indicating if profit > 0.
        - log_budget/log_revenue/log_profit: log-transformed numeric features to reduce skew.
        - popularity_z: standardized popularity score (if available).
    """
    #LOAD DATA
    try:
        df = pd.read_csv(
            file_path,
            encoding='utf-8',
            on_bad_lines='skip',
            low_memory=False  #solves dtypewarning
        )
        print("dataset loaded successfully :) first 5 rows:")
        print(df.head())
    except Exception as e:
        print("error loading dataset :( ", e)
        return None

    #DATA CLEANING
    columns_to_keep = [
        "title", "original_title", "genres", "release_date",
        "budget", "revenue", "runtime", "vote_average", "vote_count"
    ]
    df = df[columns_to_keep]
    #convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    #convert numeric columns
    numeric_cols = ['budget', 'revenue', 'runtime']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    #drop the rows without title or release_date
    df = df.dropna(subset=['title', 'release_date']).reset_index(drop=True)
    #extract genre names
    def extract_genres(genres_str):
        try:
            genres_list = ast.literal_eval(genres_str)
            return [genre['name'] for genre in genres_list]
        except (ValueError,SyntaxError):
            return []
    df['genre_names'] = df['genres'].apply(extract_genres)

    #IMPLEMENTING 7 NEW COLUMNS
    #a. main genre
    df['main_genre'] = df['genre_names'].apply(lambda x: x[0] if x else "Unknown")
    #b. release year and decade
    df['release_year'] = df['release_date'].dt.year
    df['decade'] = (df['release_year'] // 10) * 10
    #c. profit and ROI
    df['profit'] = df['revenue'] - df['budget']
    df['roi'] = df['profit'] / df['budget'].replace(0, np.nan)
    #d. runtime categories
    df['runtime_category'] = pd.cut(
        df['runtime'],
        bins=[-np.inf, 80, 120, np.inf],
        labels=['short', 'standard', 'long']
    )
    #e. is profitable?
    df['is_profitable'] = df['profit'] > 0
    #f. log transform (applying log to reduce skew. values < = 0 cannot have a logarithm, so they are set to nan).
    df['log_budget'] = np.log(df['budget'].replace(0, np.nan))
    df['log_revenue'] = np.log(df['revenue'].replace(0, np.nan))
    df['log_profit'] = df['profit'].apply(lambda x: np.log(x) if x > 0 else np.nan)
    #g. popularity standardization
    if 'popularity' in df.columns:
        df['popularity_z'] = (df['popularity'] - df['popularity'].mean()) / df['popularity'].std()
    return df