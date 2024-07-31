from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import requests
from langchain_community.tools import DuckDuckGoSearchResults
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# File-based storage path
DB_FILE = os.path.join(os.path.dirname(__file__), 'content_data.json')

def load_data():
    if os.path.exists(DB_FILE):
        logging.info(f"Loading data from {DB_FILE}")
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logging.error(f"Error loading JSON data: {e}")
            return {}
    else:
        logging.info(f"{DB_FILE} does not exist")
    return {}

def save_data(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logging.info("Data saved successfully")
    except IOError as e:
        logging.error(f"Error saving JSON data: {e}")

content_db = load_data()

search = DuckDuckGoSearchResults()

class Query(BaseModel):
    topic: str

class ContentSubmission(BaseModel):
    content_id: int

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Content Generation API"}

@app.post("/generate/")
async def generate_content(query: Query):
    ai21_api_key = os.getenv('AI21_API_KEY')
    if not ai21_api_key:
        raise HTTPException(status_code=500, detail="AI21 API key not set. Please set the environment variable 'AI21_API_KEY'.")

    url = "https://api.ai21.com/studio/v1/j2-large/complete"
    headers = {
        "Authorization": f"Bearer {ai21_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Generate content based on the topic: {query.topic}",
        "numResults": 1,
        "maxTokens": 100
    }

    try:
        logging.info(f"Making request to {url} with payload: {payload}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)  # Set timeout to 10 seconds
        response.raise_for_status()
        
        result = response.json()
        completions = result.get('completions', [])
        if not completions:
            raise HTTPException(status_code=500, detail="No completions found in response")

        text = completions[0].get('data', {}).get('text', '').strip()
        if not text:
            raise HTTPException(status_code=500, detail="Generated text is empty")

        content_id = len(content_db) + 1
        content_db[content_id] = {
            'topic': query.topic,
            'content': text
        }
        save_data(content_db)

        return {"content": text, "id": content_id}
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
        raise HTTPException(status_code=500, detail=f"Value error: {e}")
    except KeyError as e:
        logging.error(f"Key error: {e}")
        raise HTTPException(status_code=500, detail=f"Key error: {e}")

@app.post("/submit/")
async def submit_content(content: ContentSubmission):
    if content.content_id in content_db:
        content_entry = content_db[content.content_id]
        return {"detail": "Content submitted successfully", "content": content_entry}
    else:
        raise HTTPException(status_code=404, detail="Content not found")

@app.post("/search/")
async def search_content(query: Query):
    try:
        logging.info(f"Searching with query: {query.topic}")
        results = search.invoke(query.topic)
        return {"results": results}
    except Exception as e:
        logging.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
