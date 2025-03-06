# Chop.it URL Shortener

Chop.it is a simple and efficient URL shortener built with **Python, FastAPI, Streamlit, and SQLite** that enables users to quickly shorten long URLs into compact links for easy sharing.

## Features
- **Shorten long URLs**: Given a long url, a unique short url is auto generated. In case a duplicate entry of long url is provided then it is shortened to same short url.
- **Redirection**: Short URL redirects to associated original URL
- **Short URL Information Retrieval**: Given a short URL, client can obtain original URL and the click count
- **Custom short URL**: Option to provide custom short string to generate short url. Short url is also unique for each long url.
- **RESTful API**: APIs for communication between backend and frontend 
- **Track click counts**: Updates the count of clicks for each short url upon redirection
- **Simple, intuitive user interface**: Interactive UI with hints and help

## Architecture
The application consists of three main components:

### Backend API (FastAPI):
- Handles URL shortening logic
- Manages redirects and click count for short URLs
- Tracks click statistics
- Provides RESTful endpoints

### Frontend UI (Streamlit):
- User-friendly interface for shortening URLs
- View click statistics
- Custom URL input option
- Retrieve Original URL from Short URL

### Persistent Database (SQLite):
- For development purposes, using SQLite3
- Extensible design by configuring db_adapter and introducing new databases

## 🔧 Tech Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite (configurable via environment variables)
- **Deployment:** Docker with Supervisor

## 📡 API Endpoints
 
| Method | Endpoint             | Description                             |Parameters                              |
|--------|--------------------- |-----------------------------------------|----------------------------------------
| GET    | `/url/{shorturl}`    | Redirects to the original URL           |short_url: string                       |
| POST   | `/url/`              | Creates a new shortened URL             |original_url: string, short_url: string |
| GET    | `/url/count/{url}`   | Gets click count for a URL              |short_url: string                       |
| GET    | `/url/original/{url}`| Fetches the original URL using short url|short_url: string                       |


## Project Structure
```
├── backend/                 # Backend folder (FastAPI)
│   ├── main.py              # FastAPI application
│   ├── db_adapter.py        # Database adapter interface
│   ├── db_sqlite.py         # SQLite implementation
│   └── response_codes.py    # API response codes
├── ui/                      # Frontend folder (Streamlit UI)
│   └── frontend.py          # Streamlit UI
├── .env                     # Environment variables
├── Dockerfile               # Docker configuration
├── supervisord.conf         # Supervisor configuration for Docker
└── requirements.txt         # Python dependencies

```


## Setup and Installation

### Prerequisites
Ensure you have the following installed:
- **Python 3.10+**
- **pip**
- Docker (optional)

### Local Installation (Without Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/yadvendersingh/chopit.git
   cd chopit
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables or create .env file in repository:
   ```
   DB_TYPE=sqlite
   DB_NAME=urls.db
   SHORT_URL_LENGTH=8
   HOST=http://localhost
   PORT=8000
   ```

4. Run the backend in one terminal (host and port should be same as environment variables):
   ```
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

5. Run the frontend (in a separate terminal):
   ```
   streamlit run ./ui/frontend.py
   ```

6. Access the application at http://localhost:8501

### Docker Deployment
The application can be deployed using Docker:

1. Build the Docker image:
   ```
   docker build -t chopit .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 -p 8501:8501 chopit
   ```

This will start both the **FastAPI backend** and **Streamlit frontend** using Supervisor

## Usage
**Shorten URL Section**
1. Enter the long URL you want to shorten.
2. Check the "Use custom short URL" box to specify a custom short URL.
3. Click the "Shorten URL" button.
4. Copy the generated short URL to share.

**Retrieve Short URL Information**

1. To retrieve Original URL, click the "Retrieve URL" button.
2. To check click statistics, enter the short url URL and click the "Click Count" button.
