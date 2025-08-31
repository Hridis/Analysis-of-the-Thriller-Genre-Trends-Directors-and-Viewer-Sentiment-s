# Analysis of the Thriller Genre: Trends, Directors and Viewer Sentiment's
This project analyzes data from IMDb website [Click here](https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_special,video,tv_series,tv_miniseries&interests=in0000186&sort=num_votes,desc) related to the thriller genre, utilizing Selenium for web scraping and python  for data processing. A total of 250 movie records were scraped, providing insights into popular subgenres, directors, revenue trends, and user review sentiment. 
# Problem Statement

With the rise of streaming platforms and the growing popularity of thriller content, there is a need to analyze key factors driving the genre's success. 
This project investigates:

1.Popular Subgenres: Identifying the most common thriller subgenres based on viewer ratings.

2.Directors: Exploring which directors are most associated with the thriller genre.

3.Revenue Trends: Analyzing the financial success of thriller subgenres.

4.Viewer Sentiment: Extracting user review sentiment to understand how viewers feel about popular thriller content.

5.Trends over Time: Exploring how budgets, box office earnings, and ratings have evolved for thriller movies and TV shows.


# Data Processing

The data for this analysis was scraped from IMDb using Selenium. A total of 250 movie records were collected, focusing on:

Movie titles,Subgenres,Directors,Revenue figures,User review ratings and sentiment and other insights

The data was processed using Python libraries such as pandas, matplotlib to clean and analyze data.

# Dashboard
![Thriller Genre Dashboard](https://github.com/Hridis/Analysis-of-the-Thriller-Genre-Trends-Directors-and-Viewer-Sentiment-s/blob/main/Dashboard%201.png)

Tableu public view: [Click here](https://public.tableau.com/views/Book1_17565749848580/Dashboard1?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

# Findings
1. Popular Subgenres of Thriller: The most popular subgenres are Psychological Thriller, Action Thriller, and Crime Thriller.
Subgenres like Mystery and Supernatural Thriller show significant growth in user interest.

2. Most Common Directors in the Thriller Genre: Christopher Nolan, David Fincher, and Michael Bay are the most common directors in this genre, with Nolan leading in the number of thriller movies.

3. Revenue Trends: Thriller movies, especially those directed by big names, show a significant rise in revenue over the years, with certain subgenres like Action Thrillers and Crime Thrillers being particularly successful.

4. Viewer Sentiment: Viewer sentiment analysis shows that thriller movies such as Inception, The Dark Knight, and Fargo receive overwhelmingly positive reviews.Negative sentiments are often found in less popular thrillers.
5. TV Shows vs. Movies in the Thriller Genre: A comparison graph showing the average number of thriller movies and series, with movies being significantly more common but series has more average user review numbers and star rating.

6. Rising Budgets and Box Office Earnings: Budgets for thriller movies have steadily increased, with a corresponding rise in box office earnings, especially post-2000.
7. Review and Star Rating Analysis: This chart breaks down reviews by the number of reviews and star ratings for popular thriller movies, highlighting titles such as The Dark Knight and Joker.

## Build From Sources

### 1. Clone the Repository

To get started, first clone the repository:

```bash
git clone https://github.com/Hridis/A-Comprehensive-Analysis-of-the-Thriller-Genre-Trends-Directors-and-Viewer-Sentiment-s
```
### 2.Initialize and Activate Virtual Environment
```bash
virtualenv --no-site-packages venv
source venv/bin/activate
```

### 3.Install dependencies
```bash
pip install -r requirements.txt
```
### 4.Check the scrapped data
```bash
https://github.com/Hridis/Analysis-of-the-Thriller-Genre-Trends-Directors-and-Viewer-Sentiment-s/blob/main/movie%20data.csv
```
