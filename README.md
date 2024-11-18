# Project Title: Automated Web Data Extraction and LLM Query System (AI Information Retrieval Agent)

## Project Description
This project is an automated system designed to extract essential information from websites, format the data, and query a large language model (LLM) to provide concise and fact-based responses. The main functionality includes:
- Scraping structured data from websites.
- Formatting the extracted data for LLM consumption.
- Sending queries to the LLM and handling responses.

## Video Recording 
- **Loom video Link**  : https://www.loom.com/share/e5347765da674717adb7db5005982e50?sid=8ce819ed-9221-4ace-8f3a-93f6d1704d30

## Features
- **Web Scraping Module**: Extracts metadata, contact information, and social media links.
- **Data Formatting**: Processes and formats extracted data into a structured string for LLM querying.
- **LLM Integration**: Sends queries to the LLM using a provided API key and retrieves responses.
- **Error Handling and Logging**: Includes comprehensive logging and retry logic for robustness.

## Technologies Used
- **Python**
- **BeautifulSoup** and **requests** for web scraping.
- **Groq API** for LLM interaction.
- **Logging** for debugging and tracking execution.
- **Bing Search API** for searching of urls from web

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/arpitkumar2004/AI_Information_Retrieval_Agent.git

   ```
2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the main script**:
   ```bash
   python main.py
   ```
2. **Provide the required input** (e.g., URL and query). For testing purpose i have already mentioned in the file
3. **View the output**, which displays the formatted data and LLM response.

### Example
```python

file_path = r"<your_file_path>"
query = "What is the contact email for this company?"
response = query_llm_from_text(scrape_essential_info(url), query, api_key)
print(response)

```

## Configuration
- **API Key**: Ensure your Groq API and Bing Search API key is set in the environment or passed securely to the script. (for eg. add config.py in the backend/app/config.py )
- **Retry Mechanism**: Configurable number of retries and delay settings for API calls.

### Example
```python

# config.py

groq_api_key = "<your-groq-api-key>"  # Replace with your actual API key
Bing_api_key = "<you-bing-api-key>" # Replace with your OpenAI API Key

```

## Error Handling
- Handles common errors, including missing keys in the extracted data.
- Logs errors with detailed information for troubleshooting.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions, please reach out to [kumararpit17773@gmail.com].

