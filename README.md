## Wikipedia Political Leaders Scraper
# Description

This project retrieves political leaders from the Country Leaders API and scrapes the first paragraph of each leader's Wikipedia page. The collected data is stored in a JSON file.

The project was developed as part of a collaborative data engineering exercise using Git Flow, REST APIs, web scraping, and Python.

# Features
Retrieve countries and political leaders from an API
Scrape Wikipedia pages using BeautifulSoup
Clean and process text data
Export results to a JSON file
Error handling for API and scraping requests
Modular code structure

# Project Structure
wikipedia-scraper/
├── main.py
├── requirements.txt
├── README.md
├── dev/
│   ├── student_a_sandbox.ipynb
│   └── student_b_sandbox.ipynb
└── src/
    ├── __init__.py
    ├── api_client.py
    └── html_scraper.py