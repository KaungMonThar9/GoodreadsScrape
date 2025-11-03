<h1 align="center">Book Data Visualization</h1>

# Overview
This project combines Python web scraping and Tableau visualization to explore around 5,000 novels from Goodreads. Using a Python pipeline built with Playwright and BeautifulSoup, book data was collected (titles, authors, genres, publication years, ratings, and number of reviews). The cleaned dataset was then imported into Tableau Public, where a dashboard was created to analyze trends in book popularity, author output, and reader preferences across genres.

# Automated Web Scraping
- Scraped book titles, authors, genres, average ratings, and number of ratings from Goodreads.
- Built using Playwright for browser automation and BeautifulSoup for HTML parsing.
- Implemented autosaving for long scraping runs while scraping each individual book page.

# Data Cleaning and Structuring
- Converted JSON data into CSVs for seamless Tableau manipulation.
- Split combined fields (e.g., "Fantasy, Romance") into individual genres for improved data analysis.
- Added a **Document Index** to uniquely identify each book and assist with sorting purposes.
- Filtered out incomplete entries (e.g., books missing author names or publication years) for cleaner visualizations.

# Interactive Tableau Dashboard
- Created an interactive dashboard in Tableau Public sorted by genre featuring:
  - Total Books and Average Rating
  - Top Authors by Total Books
  - Heat Map of Ratings vs. Publication Year
  - Rating Distribution Histogram
  - Top Books Weighted by Rating and Number of Ratings
- Added a **genre filter** that dynamically updates all visualizations simultaneously.
- Styled the dashboard with a **neutral beige background** to match the atmosphere of a book visualization dashboard.

<img width="1291" height="763" alt="allGS" src="https://github.com/user-attachments/assets/9349131c-38f0-444d-b849-b04a63c5efb3" />

<img width="1288" height="761" alt="image" src="https://github.com/user-attachments/assets/b94ad406-670f-4562-b46b-c3ab10274107" />

## Application Set Up
- git clone https://github.com/KaungMonThar9/GoodreadsScrape.git
- cd GoodreadsScrape
- Install Playwright, BeautifulSoup, Pandas, and Python (pip install playwright beautifulsoup4 pandas)

## Tools Utilized
- BeautifulSoup
- Tableau Public
- Playwright
- Pandas
- Python
