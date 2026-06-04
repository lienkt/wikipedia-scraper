import requests
import re
from bs4 import BeautifulSoup
from requests import Session
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def fetch_html(url: str, session: Session) -> str:
  """Fetch the HTML content of a given URL.
  Args:        
    url (str): The URL to fetch.
  Returns:     
    json: The JSON content of the page, or None if an error occurs
  """

  try:

    headers = {
        "User-Agent": "MyWikiProject/1.0 (contact: lienkt0110@gmail.com)"
    }
    response = session.get(url, headers=headers, timeout=10)

    # Handle HTTP errors (404, 500, etc.)
    response.raise_for_status()
    return response.text

  except requests.exceptions.HTTPError as e:
      logger.error(
          f"HTTP error occurred: {e} "
          f"(status code: {e.response.status_code})"
      )

  except requests.exceptions.ConnectionError:
      logger.error("Connection error: failed to reach the server")

  except requests.exceptions.Timeout:
      logger.error("Timeout error: request took too long")

  except requests.exceptions.RequestException as e:
      logger.error(f"Unexpected error: {e}")

  return None

def get_first_paragraph(html: str) -> str:
  """Extract the first paragraph from the HTML content.
  Args:        
    html (str): The HTML content to parse.
  Returns:     
    str: The text of the first paragraph, or an empty string if not found.    
  """
  soup = BeautifulSoup(html, "html.parser")
  first_paragraph = ""
  content = soup.find("div", id="mw-content-text")
  if content:
    parser_output = content.find("div", class_="mw-parser-output")

    if parser_output:
      # Get all direct p in mw-parser-output
      paragraphs = parser_output.find_all("p", recursive=False)

      for p in paragraphs:
        text = p.get_text(strip=True)
        if text:  # ignore empty p
          first_paragraph = text
          break

  return first_paragraph

def clean_text(text: str) -> str:
  """Clean the extracted text by removing extra whitespace and special characters.
  Args:        
    text (str): The text to clean.
  Returns:     
    str: The cleaned text.
  """
  # Remove Wikipedia references/citations
  # Examples: [1], [12], [a], [citation needed]
  text = re.sub(r"\[[^\]]*\]", "", text)

  # Remove IPA / phonetic pronunciation blocks
  # Example: (/bəˈrɑːk oʊˈbɑːmə/)
  text = re.sub(r"\([^)]*[/ˈˌ][^)]*\)", "", text)

  # Replace common HTML entities
  text = re.sub(r"&nbsp;", " ", text)
  text = re.sub(r"&amp;", "&", text)

  # Replace multiple spaces, tabs and line breaks with a single space
  text = re.sub(r"\s+", " ", text)

  # Remove spaces before punctuation marks
  # Example: "hello ." -> "hello."
  text = re.sub(r"\s+([.,;:!?])", r"\1", text)

  return text.strip() 

def to_json_file(data: dict, filepath: str) -> None:
  """Save the data to a JSON file.
  Args:        
    data (dict): The data to save.
    filename (str): The name of the file to save to.
  Returns:     
    None
  """
  with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
