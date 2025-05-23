import os
import time
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WebSearch:
    def __init__(self, api_key=None, cooldown=None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.cooldown = cooldown or int(os.getenv("SERPER_COOLDOWN", 60))
        self.last_request_time = 0
        self.serper_url = "https://google.serper.dev/search"

        # Validate API Key
        if not self.api_key:
            raise ValueError("⚠️ SERPER_API_KEY not found. Make sure it is set in your .env file.")
        
        logging.info("✅ Serper API configuration initialized successfully.")

    def _rate_limit(self):
        elapsed_time = time.time() - self.last_request_time
        if elapsed_time < self.cooldown:
            wait_time = self.cooldown - elapsed_time
            logging.info(f"⏳ Rate limit reached. Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    def search_whitepaper(self, project_name_or_symbol, num_results=5):
        self._rate_limit()

        try:
            # Formulate the search query
            query = f"{project_name_or_symbol} white paper"
            print(f"Sending query: '{query}'")
            
            # Make direct API request to Serper instead of using wrapper
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "gl": "us",
                "hl": "en",
                "num": num_results
            }
            
            response = requests.post(self.serper_url, headers=headers, json=payload)
            
            # Debug output
            print(f"Response status code: {response.status_code}")
            
            # Check if request was successful
            if response.status_code != 200:
                logging.error(f"⚠️ API request failed with status code {response.status_code}: {response.text}")
                return {"error": f"API request failed with status code {response.status_code}"}
            
            # Parse JSON response
            try:
                results = response.json()
                print(f"Results structure keys: {list(results.keys())}")
            except json.JSONDecodeError as e:
                logging.error(f"⚠️ Failed to decode JSON response: {e}")
                print(f"Response content: {response.text[:500]}...")  # Print first 500 chars
                return {"error": f"Failed to decode JSON response: {e}"}
            
            # Extract relevant information
            extracted_results = []
            
            # Process organic results
            if "organic" in results:
                for item in results["organic"][:num_results]:
                    extracted_results.append({
                        "title": item.get("title", "No title"),
                        "snippet": item.get("snippet", "No snippet"),
                        "link": item.get("link", "No link")
                    })
            
            # Process knowledge graph results if available and needed
            if "knowledgeGraph" in results and not extracted_results:
                kg = results["knowledgeGraph"]
                extracted_results.append({
                    "title": kg.get("title", "Knowledge Graph"),
                    "snippet": kg.get("description", "No description"),
                    "link": kg.get("website", "No link")
                })
            
            self.last_request_time = time.time()
            logging.info(f"✅ Successfully fetched {len(extracted_results)} results for project: {project_name_or_symbol}")
            return extracted_results

        except Exception as e:
            logging.error(f"⚠️ API Error: {e}")
            return {"error": str(e)}