# Anatomy of a Blockbuster: Exploratory Analysis of Movies
This project explores the factors that contribute to a movie’s success using a comprehensive dataset of films. 
By analyzing budget, revenue, profit, genres, and audience ratings, we investigate trends, outliers, and the dynamics of blockbuster cinema. 
The analysis includes temporal trends, genre comparisons, and a final “blockbuster success map.”  
The main goal of this project is to understand the economic and creative patterns that determine a movie’s financial and critical success. 
Key questions include:  
- How do budgets, revenues, and profits evolve over time?  
- Which genres are the most profitable and most produced?  
- What is the relationship between budget, revenue, and audience ratings?  
- How do blockbusters differ from average films in terms of revenue, budget, and ROI?  

the analysis uses **The Movies Dataset** from Kaggle, which contains:  
- Movie metadata (titles, release dates, genres, runtimes...)    
- audience ratings  
> dataset source: [The Movies Dataset on Kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)  
the dataset is loaded and preprocessed using `load_and_clean_data.py`, ensuring clean and reliable data for the visualizations created with Matplotlib and Seaborn.
all dependencies are listed in `requirements.txt`.


project structure  
anatomy_of_blockbuster/
│
├── data/                       #raw CSV dataset
│   └── movies_metadata.csv
│
├── src/                        #custom python scripts
│   └── load_and_clean_data.py  #function to load and clean dataset
│
├── notebooks/                  #jupyter notebooks
│   └── blockbuster_analysis.ipynb
|   └── images                  #images used in the notebook
│
├── outputs/                    #generated plots and figures
│
├── requirements.txt            #python libraries
└── README.md                   #project documentation

