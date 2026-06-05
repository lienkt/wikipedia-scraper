import requests
import re
from bs4 import BeautifulSoup
from requests import Session
import json
import logging
import unicodedata

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class HTMLScraper:
  """HTMLScraper is responsible for fetching and parsing HTML content from Wikipedia pages.
   It handles fetching the HTML, extracting the first paragraph, cleaning the text, and saving it to a JSON file.
   """
  def __init__(self, session: Session):
    """Initialize the HTML scraper with a requests session."""
    self.session = session

  def fetch_html(self, url: str) -> str | None:
    """Fetch the HTML content of a given URL.
    Args:        
      url (str): The URL to fetch.
    Returns:     
      str | None: HTML content or None if an error occurs.
    """
    try:
      response = self.session.get(url, timeout=10)

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
  
  @staticmethod
  def normalize(text):
    """Normalize text by removing accents and converting to lowercase.
    Args:        
      text (str): The text to normalize.
    Returns:     
      str: The normalized text.
    """
    text = unicodedata.normalize("NFD", text)
    # remove accents by filtering out characters with the "Mn" (Mark, Nonspacing) Unicode category
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")  
    text = text.lower()
    return text
  
  def get_first_paragraph(self, html: str | None) -> str:
    """Extract the first paragraph from the HTML content.
    Args:        
      html (str): The HTML content to parse.
    Returns:     
      str | None: The first paragraph text or an empty string if not found.   
    """
    if not html:
        return ""
    
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="mw-content-text")
    h1 = soup.find("h1", id="firstHeading")
    span = h1.find("span", class_="mw-page-title-main") if h1 else None
    page_title = span.get_text(strip=True) if span else ""
    if "," in page_title:
        title_first_word = page_title.split(",", 1)[0].strip()
    else:
        parts = page_title.split()
        title_first_word = parts[0] if parts else ""
    if content:
      parser_output = content.find("div", class_="mw-parser-output")
      if parser_output:
        for p in parser_output.find_all("p"):
          text = p.get_text(strip=True)

          if text and len(text) > 100:
            b_tag = p.find("b")

            if b_tag:
              bold_text = b_tag.get_text()
              if self.normalize(title_first_word) in self.normalize(bold_text):
                return text

    return ""
  
  @staticmethod
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

  @staticmethod
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
