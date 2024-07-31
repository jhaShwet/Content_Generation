from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import requests

app = FastAPI()

# File-based storage path
DB_FILE = 'content_data.json'

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            print(f"Error loading JSON data: {e}")
            return {}
    return {}

def save_data(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving JSON data: {e}")

content_db = load_data()

def search_duckduckgo(query: str):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('RelatedTopics', [])
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

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
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        completions = result.get('completions', [])
        if not completions:
            raise HTTPException(status_code=500, detail="No completions found in response")

        text = completions[0].get('data', {}).get('text', '').strip()
        if not text:
            raise HTTPException(status_code=500, detail="Generated text is empty")

        # Save generated content in a JSON file or in-memory storage
        content_id = len(content_db) + 1
        content_db[content_id] = {
            'topic': query.topic,
            'content': text
        }
        save_data(content_db)

        return {"content": text, "id": content_id}
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
        raise HTTPException(status_code=500, detail=f"Value error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
        raise HTTPException(status_code=500, detail=f"Key error: {e}")

@app.post("/submit/")
async def submit_content(content: ContentSubmission):
    if content.content_id in content_db:
        content_entry = content_db[content.content_id]
        save_data(content_db)
        return {"detail": "Content submitted successfully", "content": content_entry}
    else:
        raise HTTPException(status_code=404, detail="Content not found")
