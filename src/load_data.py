import pandas as pd

# Path to the CSV file
file_path = "/Users/keithown/Documents/universidad (locale)/anatomy_of_a_blockbuster/data/movies_metadata.csv"

try:
    # Read the full dataset
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    
    # Show first rows and dataset info
    print("First rows of the dataset:")
    print(df.head())
    print("\nDataset info:")
    print(df.info())

except Exception as e:
    print("Error reading CSV:", e)



# -------------------------------------------------------------------------------
# DATA CLEANING
# ------------------------------------------------------------------------------
columns_to_keep = [
    "title", "original_title", "genres", "release_date",
    "budget", "revenue", "runtime", "vote_average", "vote_count"
]
df = df[columns_to_keep]

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce')
df = df.dropna(subset=['title', 'release_date']).reset_index(drop=True)

print("\nCleaned dataset (first rows):")
print(df.head())




# -----------------------------
# EXTRACT GENRES
# -----------------------------
# Function to extract genre names from the JSON-like string
def extract_genres(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)  # convert string to list of dicts
        return [genre['name'] for genre in genres_list]
    except:
        return []  # return empty list if parsing fails

# Apply function to create a new column with list of genre names
df['genre_names'] = df['genres'].apply(extract_genres)
# Show first rows to check
print("\nGenres extracted (first rows):")
print(df[['title', 'genre_names']].head())    





# -----------------------------
# COUNT GENRES
# -----------------------------
all_genres = [genre for sublist in df['genre_names'] for genre in sublist]
genre_counts = Counter(all_genres)

genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])
genre_counts_df = genre_counts_df.sort_values(by='Count', ascending=False)



# -----------------------------
# PLOT TOP 10 GENRES
# -----------------------------
sns.set_style("darkgrid")
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["figure.figsize"] = (12, 7)

top_genres = genre_counts_df.head(10)
ax = sns.barplot(x="Count", y="Genre", data=top_genres, palette="coolwarm", edgecolor="black")

ax.set_title("Top 10 Movie Genres – A Cinephile’s Perspective 🎥", fontsize=18, fontweight='bold')
ax.set_xlabel("Number of Movies", fontsize=14)
ax.set_ylabel("Genre", fontsize=14)

# Add number labels on bars
for i, v in enumerate(top_genres['Count']):
    ax.text(v + 50, i, str(v), color='black', fontweight='bold')

plt.tight_layout()
plt.show()