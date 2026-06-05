import requests
class APIClient:
  """APIClient is responsible for communicating with the country leaders API.
   It handles fetching the list of countries and their leaders, as well as managing cookies for authentication.
   """
  def __init__(self, config: dict):
    """Initialize the API client with configuration.
    args:
      config (dict): A dictionary containing API configuration, including base URL and endpoints. 
    """
    self.base_url = config["base_url"].rstrip("/")
    self.country_endpoint = config["country_endpoint"]
    self.leaders_endpoint = config["leaders_endpoint"]
    self.cookies_endpoint = config["cookies_endpoint"]
    self.session = requests.Session()
    self.refresh_cookie()
    
          
  def refresh_cookie(self) -> None:
        """Fetch and store fresh cookies in the session."""
        url = f"{self.base_url}{self.cookies_endpoint}"
        response = self.session.get(url)
        response.raise_for_status()

        # Session automatically stores cookies
        return

  def get_countries(self) -> list:
    """Fetch the list of countries from the API.
      Returns:
        list: A list of country names obtained from the API.
      """
    self.refresh_cookie()

    response = self.session.get(
            f"{self.base_url}{self.country_endpoint}"
        )
    response.raise_for_status()
    return response.json()

  def get_leaders(self, country: str) -> list:
    """Fetch the list of leaders for a given country from the API.
    Args:
      country (str): The name of the country for which to fetch leaders.  
    Returns:
      list: A list of leaders for the specified country obtained from the API.
    """
    self.refresh_cookie()

    response = self.session.get(
    f"{self.base_url}{self.leaders_endpoint}",
            params={"country": country}
        )
    response.raise_for_status()
    return response.json()