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
    self.base_url = config["base_url"]
    self.country_endpoint = config["country_endpoint"]
    self.leaders_endpoint = config["leaders_endpoint"]
    self.cookies_endpoint = config["cookies_endpoint"]
    self.session = requests.Session()
    self.session.headers.update({
        "User-Agent": config["user_agent"]
    })
          
  def refresh_cookie(self) -> None:
    """Fetch a new cookie from the API and store it for future requests.
    """
    response = self.session.get(f"{self.base_url}{self.cookies_endpoint}")
    response.raise_for_status()

  def _ensure_cookie(self) -> None:
      """Ensure that a valid cookie is available for API requests. If not, refresh the cookie."""
      if not self.session.cookies:
          self.refresh_cookie()

  def get_countries(self) -> list:
    """Fetch the list of countries from the API.
      Returns:
        list: A list of country names obtained from the API.
      """
    self._ensure_cookie()

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
    self._ensure_cookie()

    response = self.session.get(
        f"{self.base_url}{self.leaders_endpoint}",
        params={"country": country}
    )
    response.raise_for_status()
    return response.json()