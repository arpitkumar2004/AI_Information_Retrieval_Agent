import pandas as pd
import requests as r
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded data or None if an error occurs.
    """
    try:
        # Attempt to read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully!")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None


# def get_user_query() -> str:
#     """
#     Prompt the user to enter a query.
    
#     Returns:
#         str: The query input by the user.
#     """
#     while True:
#         query = input("Please enter the information you need (e.g., 'Get me the email of the company'): ")
        
#         # Ensure the query is not empty
#         if query.strip():
#             return query
#         else:
#             logging.warning("Invalid input. Please enter a valid query.")


def search_urls(query: str, api_key: str) -> list:
    """
    Search for URLs based on the user's query using the Bing Search API.
    
    Args:
        query (str): The query string to search.
        api_key (str): The Bing Search API key.
    
    Returns:
        list: List of URLs returned by the search.
    """
    try:
        logging.info("Initiating search...")
        # Construct the search URL and headers for the API request
        search_url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        params = {"q": query, "textDecorations": True, "textFormat": "HTML"}

        # Make the API request
        response = r.get(search_url, headers=headers, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            urls = [result['url'] for result in data.get('webPages', {}).get('value', [])]
            # logging.info(f"Found {len(urls)} URLs for query: '{query}'")
            return urls
        else:
            logging.error(f"Failed to retrieve data (Status Code: {response.status_code})")
            return []
    
    except Exception as e:
        logging.error(f"Error during search: {e}")
        return []


if __name__ == "__main__":
    # Example usage:
    try:
        # Load data and get a query from the user
        # file_path = input("Enter the path to your CSV file: ")
        file_path = r'C:\Users\RDRL\Desktop\Desktop\Checkit\Project BreakoutAI - front-end\project\backend\app\uploads\test csv - Sheet1.csv'
        df = load_data(file_path)
        
        if df is not None:
            # query = get_user_query()
            # Example: Query formed from the first entry in the DataFrame
            query = f"Get me contact information of {df[df.columns[0]][0]}."
            
            # Search for URLs based on the query
            api_key = "fdc2c93a856043db8f1717ada9f7c8dc"  # Replace with your actual API key
            search_results = search_urls(query, api_key)
            
            if search_results:
                logging.info(f"Search results: {search_results}")
            else:
                logging.warning("No search results found.")
        else:
            logging.error("No data loaded. Please check the file path and try again.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")


