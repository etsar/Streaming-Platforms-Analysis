# Streaming Platforms Analysis
## Objective
Uncover trends in streaming content across major platforms to analyze viewer preferences and industry trends.

## Dataset
The dataset encompasses 22,619 titles and 326,177 credits, providing a comprehensive view of content available on four major streaming platforms from 1912 to 2023, including Netflix, Amazon Prime Video, Hulu, Disney+.
### Data Scraping
- Extracted data from [JustWatch](https://www.justwatch.com/) using a modified [script](https://github.com/victor-soeiro/WebScraping-Projects/blob/main/08%20-%20justwatch/main.ipynb) for content of these 4 platforms up to year 2023.
- Obtained 8 files: titles and credits for each platform.
### Data Preprocessing
- Concatenated data from 4 platforms into unified dataset.
- Standardized and cleaned data, including:
  - Replacing missing values in important columns (e.g., `age_certification`, `genres`, `production_countries`, `imdb_score`, `imdb_votes`, `seasons`).
  - Removing unnecessary columns (e.g., `tmdb_popularity`, `tmdb_score`).
- Saved as 2 consolidated csv files: `titles_all.csv` and `credits_all.csv`.
### Columns Overview
- `titles_all.csv` has the following columns:
  - `id`: The title ID on JustWatch.
  - `title`: The name of the title.
  - `show_type`: TV show or movie.
  - `description`: A brief description.
  - `release_year`: The release year.
  - `age_certification`: The age certification.
  - `runtime`: The length of the episode (SHOW) or movie.
  - `genres`: A list of genres.
  - `production_countries`: A list of countries that produced the title.
  - `seasons`: Number of seasons if it's a SHOW.
  - `imdb_id`: The title ID on IMDB.
  - `imdb_score`: Score on IMDB.
  - `imdb_votes`: Votes on IMDB.
  - `platform`: streaming platform.
 
- `credits_all.csv` has the following columns:
  - `person_ID`: The person ID on JustWatch.
  - `id`: The title ID on JustWatch.
  - `name`: The actor or director's name.
  - `character_name`: The character name.
  - `role`: ACTOR or DIRECTOR.
  - `platform`: streaming platform.
### Entity Relationship Diagram
<img src="https://github.com/etsar/Streaming-Platforms-Analysis/assets/94500188/79ed762a-143f-4d30-bb47-2db93f8d317d" alt="Entity Relationship Diagram" width="300"/>

## Tools & Technologies
- Python (Jupyter Notebook) for data scraping and preprocessing. [View Data Preprocessing Notebook](https://github.com/etsar/Streaming-Platforms-Analysis/blob/main/credits_and_titles_preprocessing.ipynb) and [View Data Scraping Script](https://github.com/etsar/Streaming-Platforms-Analysis/blob/main/justwatch_webscrapping.py).
- SQL (Snowflake) for complex data queries and analysis. [View SQL Queries](https://github.com/etsar/Streaming-Platforms-Analysis/blob/main/SQL_queries_streaming_insights.ipynb).
- Tableau for interactive visualizations.

## Insights
- Revealed Amazon's extensive content library versus Disney's targeted niche approach.
- Highlighted Netflix's balanced approach in content diversity and high ratings.

## Team Collaboration
Worked within a team of 5, dividing tasks for a comprehensive approach.
