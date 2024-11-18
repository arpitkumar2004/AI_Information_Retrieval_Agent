import time
import logging
from typing import Dict
from groq import Groq
from scraping import scrape_essential_info


# Configure logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def format_scraped_data(extracted_data: Dict) -> str:
    """
    Format the extracted structured data into a readable string for querying the LLM.

    Args:
        extracted_data (dict): The structured data extracted from the scrape_essential_info function.

    Returns:
        str: A formatted string representing the structured content.
    """
    try:
        # Extract metadata and format it
        metadata_section = f"Website URL: {extracted_data['metadata']['website_url']}\n" \
                           f"Page Title: {extracted_data['metadata']['page_title']}\n" \
                           f"Industry/Sector: {extracted_data['metadata']['industry_sector']}\n"

        # Extract contact information and format it
        contact_info_section = "Contact Information:\n"
        contact_info_section += f"Emails: {', '.join(extracted_data['contact_information']['emails'])}\n"
        contact_info_section += f"Phone Numbers: {', '.join(extracted_data['contact_information']['phone_numbers'])}\n"
        contact_info_section += f"Addresses: {', '.join(extracted_data['contact_information']['addresses'])}\n"

        # Extract and format social media links
        social_media_section = "Social Media Links:\n" + "\n".join(extracted_data['social_media'])

        # Combine all sections into one string
        scraped_text = f"{metadata_section}\n{contact_info_section}\n{social_media_section}"
        logging.info("Formatted scraped data for LLM query.")
        return scraped_text

    except KeyError as e:
        logging.error(f"Missing key in extracted data: {e}")
        raise ValueError(f"Error: Missing key in extracted data - {e}")
    except Exception as e:
        logging.error(f"An error occurred while formatting scraped data: {e}")
        raise RuntimeError("An error occurred while processing the data.")


def query_llm_from_text(extracted_data: Dict, query: str, api_key: str, retries: int = 2, delay: int = 10) -> str:
    """
    Function to query the LLM with structured extracted data.

    Args:
        extracted_data (dict): The structured data from scrape_essential_info function.
        query (str): The query for the LLM based on the extracted content.
        api_key (str): API key for accessing the LLM.
        retries (int): Number of retries in case of failure (default is 3).
        delay (int): Delay in seconds between retries (default is 10).

    Returns:
        str: The answer from the LLM based on the query.
    """
    model = "llama3-8b-8192"
    client = Groq(api_key=api_key)

    try:
        # Format the extracted data into a readable string
        scraped_text = format_scraped_data(extracted_data)
        # scraped_text = extracted_data
        
        logging.info(f"Data fromatted Succesfully....")

        # Prepare the message for the LLM
        messages = [
            {"role": "system", "content": "When asked for information, respond strictly with the factual data requested. Do not provide any extra context, elaboration, or explanation. The answer should be in the simplest form possible—just the specific data without additional commentary. If asked for an email address, respond only with the email itself, such as 'email@company.com'. If a phone number is requested, respond only with the phone number, like '123-456-7890'. The goal is to focus purely on the raw information without any accompanying text or clarifications."},
            {"role": "user", "content": f"Content:\n\n\"\"\"\n{scraped_text}\n\"\"\"\n\nQuestion: {query}"}
        ]

        # Retry logic for querying the LLM
        for attempt in range(retries):
            try:
                logging.info(f"Attempting to query LLM (Attempt {attempt + 1} of {retries})...")

                # Send request to Groq API
                response = client.chat.completions.create(
                    messages=messages,
                    model=model,
                    max_tokens=8000,  # Adjust as needed based on expected response length
                    temperature=0,   # Set to 0 for factual responses
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                # Log the response for inspection
                logging.debug(f"Response structure: {response}")

                # Assuming the response is an object, use a method or attribute to access the content
                # Replace this line with the appropriate way to get the answer from the response object
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    answer = response.choices[0].message.content.strip()  # Adjust based on actual response structure
                    logging.info("LLM query successful.")
                    return answer
                else:
                    raise ValueError("No choices in response. Unable to retrieve answer.")

            except Exception as e:
                logging.error(f"Error occurred during LLM query (Attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    logging.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logging.warning(f"Max retries reached. Unable to complete the query.")
                    return "Rate limit exceeded or unable to complete the query. Please try again later."

    except ValueError as e:
        logging.error(f"Error during data processing: {e}")
        return str(e)
    except Exception as e:
        logging.error(f"Unexpected error during LLM query process: {e}")
        return "An unexpected error occurred."





if __name__ == "__main__":
    # Example for testing the module functionality
    # test_data = {
    #     "metadata": {
    #         "website_url": "https://example.com",
    #         "page_title": "Example Company",
    #         "industry_sector": "Technology"
    #     },
    #     "contact_information": {
    #         "emails": ["contact@example.com", "support@example.com"],
    #         "phone_numbers": ["+1-800-555-1234"],
    #         "addresses": ["1234 Example St, City, Country"]
    #     },
    #     "social_media": [
    #         "https://twitter.com/example",
    #         "https://facebook.com/example"
    #     ]
    # }
    
    
    # Example url and query
    url = "https://www.ril.com/contact-us"
    test_data= scrape_essential_info(url=url)
    
    api_key = "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"
    
    query = "what is email this company?"
    
    # response= format_scraped_data(test_data)
    # print(format_scraped_data(test_data)
    response = query_llm_from_text(test_data, query, api_key)

    print(response)

