#SETUP
#the first thing we do is import the required libraries.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter
#set a different style for my plots.
sns.set_style("darkgrid")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.figsize"] = (12, 7)
#load the dataset, which is a CSV file containing metadata for 45,000 movies.
file_path = "../data/movies_metadata.csv"
try:
    df = pd.read_csv(
        file_path,
        encoding='utf-8',
        on_bad_lines='skip',
        low_memory=False  # evita DtypeWarning
    )
    print("dataset loaded successfully, first 5 rows")
    display(df.head())
except Exception as e:
    print("error loading dataset :( ", e)


#DATA CLEANING
#we want to keep only relevant columns
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
#drop rows without title or release_date
df = df.dropna(subset=['title', 'release_date']).reset_index(drop=True)
#extract genre names
def extract_genres(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)
        return [genre['name'] for genre in genres_list]
    except:
        return []
df['genre_names'] = df['genres'].apply(extract_genres)
#display cleaned data
df.sample(6, random_state=69)


#IMPLEMENTING NEW COLUMNS
import numpy as np
#a.main genre
df['main_genre'] = df['genre_names'].apply(lambda x: x[0] if x else "Unknown")
#b.release year and decade
df['release_year'] = df['release_date'].dt.year
df['decade'] = (df['release_year'] // 10) * 10
#c.profit and roi
df['profit'] = df['revenue'] - df['budget']
df['roi'] = df['profit'] / df['budget'].replace(0, np.nan)
#d.runtime categories
df['runtime_category'] = pd.cut(
    df['runtime'],
    bins=[-np.inf, 80, 120, np.inf],
    labels=['Short', 'Standard', 'Long']
)
#5.is profitable
df['is_profitable'] = df['profit'] > 0
#6.log transform
df['log_budget'] = np.log(df['budget'].replace(0, np.nan))
df['log_revenue'] = np.log(df['revenue'].replace(0, np.nan))
df['log_profit'] = df['profit'].apply(lambda x: np.log(x) if x > 0 else np.nan)
#7.popularity standardization
if 'popularity' in df.columns:
    df['popularity_z'] = (df['popularity'] - df['popularity'].mean()) / df['popularity'].std()
#final check
df.head()