from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import time
import logging
from query import search_urls ,load_data
from scraping import scrape_essential_info
from LLM_groq import query_llm_from_text
from config import Bing_api_key, groq_api_key

# Configure logging for better debugging and tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
    
@app.route('/api/process', methods=['POST'])
def process_file():
    logs = []  # List to collect logs

    # Check for the presence of a file in the request
    if 'file' not in request.files:
        logs.append("Error: Please upload a file.")
        return jsonify({"error": "Please upload a file.", "logs": logs}), 400
    
    file = request.files['file']
    
    # Extract query and column information from the form
    query = request.form.get('query', None)
    if not query:
        logs.append("Error: Query parameter is missing.")
        return jsonify({"error": "Query parameter is missing.", "logs": logs}), 400

    results = {}
    
    selected_column = request.form.get('column', 'entity')  # Default to 'entity' if no column specified

    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Read the CSV file into a DataFrame
        df = load_data(file_path)

        # Check if the selected column exists in the DataFrame
        if selected_column not in df.columns:
            logs.append(f"Error: Column '{selected_column}' not found in the file.")
            return jsonify({"error": f"Column '{selected_column}' not found in the file.", "logs": logs}), 400

        # Extract unique entities from the selected column
        entities = df[selected_column].dropna().unique()
        if len(entities) == 0:
            logs.append(f"Error: No valid entities found in column '{selected_column}'.")
            return jsonify({"error": f"No valid entities found in column '{selected_column}'.", "logs": logs}), 400

        # Process each entity
        for entity in entities:
            # Formulate the query
            query_new = f"{query} {entity}"
            logs.append(f"Processing query for: {entity}")
            logging.info("Query Loaded.")

            # Process query to get relevant web content
            logging.info("Urls search initialised....")
            url = search_urls(query,Bing_api_key)[0]
            
            logging.info("Extraction of Data initilised.....")
            extracted_text = scrape_essential_info(url)
            logging.info("Data Extraction is Completed.")
            
            if extracted_text == "notfound":
                logs.append(f"No relevant data found for {entity}.")
                results[entity] = "notfound"
                continue

            # Query the LLM with the extracted content to retrieve the required information
            llm_response = query_llm_from_text(extracted_text,query=query_new,api_key=groq_api_key)
            
            if llm_response == "LLM error":
                logs.append(f"LLM error occurred while processing {entity}.")
                results[entity] = "LLM error"
            else:
                results[entity] = llm_response
                     
        # results = {
        #         "Reliance": "contact@reliance.com",
        #         "Meta": "meta@techinc.com",
        #         "OpenAI": "contact@openai.com",
        #         # Add more mappings as needed
        #         }
        
        
        # Create the final response structure
        final_results = []
        
        for entity in entities:
            email = results.get(entity, "notfound")
            final_results.append({
                "entity": entity,
                "email": email,
                "status": "success" if email != "notfound" else "Not found"
            })

        # Send the final results along with the logs
        return jsonify({"results": final_results, "logs": logs}), 200

    except Exception as e:
        logs.append(f"Error: {str(e)}")  # Log the exception error
        return jsonify({"error": f"An error occurred while processing the file: {str(e)}", "logs": logs}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
