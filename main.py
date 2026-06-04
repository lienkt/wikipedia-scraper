
import os
import json
from src.api_client import APIClient
from src.html_scraper import clean_text, fetch_html, get_first_paragraph, to_json_file
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
  """
  Main entry point of the seating application.

  This program:
  1. Loads configuration from a JSON file.
  """
  # ---------------------------------------
  # Load configuration file
  # ---------------------------------------
  # Get project base directory
  base_dir = os.path.dirname(__file__)
  config_filepath = os.path.join(base_dir, "config.json")
  output_filepath = os.path.join(base_dir, "leader.csv")
  with open(config_filepath, "r", encoding="utf-8") as f:
    config = json.load(f)

  # ---------------------------------------
  # Choose input file mode
  # ---------------------------------------
  print("\n=== Choose output file type to store the list of leaders ===")
  print("1. CSV")
  print("2. JSON")

  while True:
    choise_filepath = input("Choose an option: ")

    if choise_filepath == "2":
      output_filepath = os.path.join(base_dir, "leader.json")
    if not choise_filepath in ["1","2"]:
      logger.info("Options are 1 or 2. Please choose again.")
      continue
    break

  # ---------------------------------------
  # Get countries and leaders from API
  # ---------------------------------------
  logger.info("Fetching data from API...")
  api_client = APIClient(config)
  countries = api_client.get_countries()
  leaders_per_country = {}
  for country in countries:
    logger.info(f"Fetching leaders for {country}...")
    leaders = api_client.get_leaders(country)

    for leader in leaders:
        logger.info(f"Processing {leader['first_name']} {leader['last_name']} from {country}...")
        html = fetch_html(leader["wikipedia_url"], api_client.session)
        leader["intro"] = clean_text(get_first_paragraph(html))

    leaders_per_country[country] = leaders

  # ---------------------------------------
  # Save leaders of countries to JSON file
  # ---------------------------------------
  logger.info(f"Saving data to {output_filepath}...")
  to_json_file(leaders_per_country, output_filepath)

# ---------------------------------------
# Program entry point
# ---------------------------------------
if __name__ == "__main__":
    main()
