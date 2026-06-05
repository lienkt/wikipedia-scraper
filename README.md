# Wikipedia Political Leaders Scraper
## Description

This project retrieves political leaders from the Country Leaders API and scrapes the first paragraph of each leader's Wikipedia page. The collected data is stored in a JSON file.

The project was developed as part of a collaborative data engineering exercise using Git Flow, REST APIs, web scraping, and Python.
![webscraping_image](https://sm.pcmag.com/t/pcmag_au/news/w/wikipedia-/wikipedia-is-now-25-years-old-citation-not-needed_98t3.1920.jpg)
## Features

- Retrieve countries and political leaders from an API
- Scrape Wikipedia pages using BeautifulSoup
- Clean and process text data
- Export results to a JSON or CSV file
- Error handling for API and scraping requests
- Modular code structure

## Project Structure
```text
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
```
## Architecture

The project is split into independent modules:

- api_client.py → Handles all API communication
- html_scraper.py → Handles HTML fetching and parsing
- main.py → Orchestrates the full pipeline

##  Architecture Diagram

```mermaid
flowchart TB

    USER[User]

    USER --> MAIN[main.py]

    MAIN --> CONFIG[config.json]

    MAIN --> API[APIClient]

    API --> COUNTRY_API[Country Leaders API]

    MAIN --> SCRAPER[html_scraper.py]

    SCRAPER --> WIKI[Wikipedia Pages]

    COUNTRY_API --> API
    WIKI --> SCRAPER

    API --> MAIN
    SCRAPER --> MAIN

    MAIN --> OUTPUT[leader.json / leader.csv]
```

```mermaid

```
## Workflow
- API client fetches country list
- For each country → fetch leaders
- Extract Wikipedia URLs
- Scraper downloads HTML pages
- Extract first valid paragraph
- Clean text and structure data
- Save final dataset

## Component Architecture


```mermaid
classDiagram

    class main {
        +main()
    }

    class APIClient {
        +get_countries()
        +get_leaders(country)
        +refresh_cookie()
    }

    class html_scraper {
        +fetch_html()
        +get_first_paragraph()
        +clean_text()
        +to_json_file()
    }

    class config {
        config.json
    }

    class output {
        leader.json
        leader.csv
    }

    main --> config
    main --> APIClient
    main --> html_scraper
    main --> output
```
## Installation

-  Clone the repository
-  Create a virtual environment 
-  Activate the virtual environment
-  Install dependencies

## Requirements

- Python 3.10+
- requests
- beautifulsoup4

## Usage

Run the full pipeline:
```
python main.py
```
The script will:

- Load API configuration from config.json
- Connect to the Country Leaders APIRetrieve all available countries
- Retrieve leaders for each country
- Scrape each leader's Wikipedia page
- Extract and clean the first meaningful paragraph
- Add the biography to the leader record
- Export the results to either:
```
leader.csv
leader.json
```
## Acknowledgements

This project was completed as part of the **AI Bootcamp** at **BeCode.org**. The assignment focused on applying software engineering best practices, including Git Flow collaboration, API integration, web scraping, data processing, and modular Python development.

## Contributors

- 1. Lien Kim
- 2. Sitara Sachidanandan



