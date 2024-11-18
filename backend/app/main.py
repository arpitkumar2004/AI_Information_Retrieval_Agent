from query import search_urls,load_data
from scraping import scrape_essential_info
from LLM_groq import query_llm_from_text
from config import Bing_api_key, groq_api_key

def main():
   
    query = "Get me support or contact email of "

    # Pipeline
    url = search_urls(query,Bing_api_key)[0]
    scrapped_text = scrape_essential_info(url)
    result = query_llm_from_text(scrapped_text,query, api_key=groq_api_key)
    print(result)

    # file_path= r'C:\Users\RDRL\Desktop\Desktop\Checkit\Project BreakoutAI - front-end\project\backend\app\uploads\test csv - Sheet1.csv'
    # df = load_data(file_path)
    
    # selected_column = df.columns[0]
    # # Extract unique entities from the selected column
    # entities = df[selected_column]
    
    # results = {}
    # for entity in entities:
    #     # Formulate the query
    #     query_new = f"{query} {entity}"

    #     # Process query to get relevant web content

    #     url = search_urls(query,Bing_api_key)[0]
        

    #     extracted_text = scrape_essential_info(url)

        
    #     if extracted_text == "notfound":

    #         results[entity] = "notfound"
    #         continue

    #     # Query the LLM with the extracted content to retrieve the required information
    #     llm_response = query_llm_from_text(extracted_text,query=query_new,api_key=groq_api_key)
        
    #     if llm_response == "LLM error":
    #         results[entity] = "LLM error"
    #     else:
    #         results[entity] = llm_response

    # # Create the final response structure
    # final_results = []
    
    # for entity in entities:
       
    #     email = results.get(entity, "notfound")
    #     final_results.append({
    #         "entity": entity,
    #         "email": email,
    #         "status": "success" if email != "notfound" else "Not found"
    #     })
    #     print(f'# {entity} ------- {email}')
        

if __name__ == "__main__":
    main()
