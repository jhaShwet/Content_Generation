# Content_Generation
ContentCraft is a FastAPI and Streamlit-based application that generates content based on user-specified topics using the AI21 API. The backend leverages FastAPI to handle content generation requests, while the frontend uses Streamlit to provide a user-friendly interface for generating and displaying content.

## Tech Stack

### Backend: https://content-backend2.onrender.com/

- **FastAPI**: High-performance web framework for APIs.
- **Uvicorn**: ASGI server for FastAPI.
- **Pydantic**: Data validation and settings management.
- **Requests**: HTTP library for API requests.
- **API Endpoints**: Configure the requests on Postman.

    - **Root Endpoint**
    - **Generate Content**: `curl -X POST "[https://backend-app1-0icr.onrender.com](https://content-backend2.onrender.com/)/generate/" -H "Content-Type: application/json" -d '{"topic": "Python"}'`
    - **Search Content**: `curl -X POST "[https://backend-app1-0icr.onrender.com](https://content-backend2.onrender.com/)/search/" -H "Content-Type: application/json" -d '{"topic": "Python"}'`
    - **Submit Content**: `curl -X POST "[https://backend-app1-0icr.onrender.com](https://content-backend2.onrender.com/)/submit/" -H "Content-Type: application/json" -d '{"content": "Generated content here"}'`

### Frontend:  https://content-frontend-0ji5.onrender.com/

- **Streamlit**: Framework for interactive web applications.
- **Functionality**:
    - Allows users to generate content.
    - Provides a search feature for related topics.
    - Submits user-generated content.

## Database

- **JSON File**: Storage for generated content and user submissions.

## Hosting

- **GitHub**: https://github.com/jhaShwet/Content_Generation
- **Render**: Deployment of the application
- **Features**:
    - Generate content on a given topic.
    - Search for related topics.
    - Submit generated content.
    - User-friendly interface with Streamlit.

## Prerequisites

- Python 3.8+
- pip for package management
- AI21 API key

