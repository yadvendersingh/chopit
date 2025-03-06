from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse, JSONResponse
from backend.db_adapter import *
from pydantic import BaseModel
from urllib.parse import urlparse
from backend.response_codes import ResponseCodes

app = FastAPI()

# URLObject class for input
class URLObject(BaseModel):
    original_url: str
    short_url: str

# API Endpoint for redirection of short url
@app.get("/url/{short_url}")
async def redirect(short_url: str):
    response, original_url = get_url_by_short(short_url)
    if response == ResponseCodes.NOT_FOUND:
        return JSONResponse(status_code=response.value["code"], content={"message": "Short URL not found!"})
    increment_clicks(short_url)
    return RedirectResponse(url=original_url[0])

#API Endpoint for getting original URL
@app.get("/url/original/")
async def get_original_url(short_url: str):
    response, original_url = get_url_by_short(short_url)
    if response == ResponseCodes.NOT_FOUND:
        return JSONResponse(status_code=response.value["code"], content={"message": "Short URL not found!", "original_url": ""}) 
    return JSONResponse(status_code=response.value["code"], content={"message": "Original URL", "original_url": original_url[0]})

#API Endpoint for shortening URL and storing in DB
@app.post("/url/")
async def shorten_url(input: URLObject):
    if not is_valid_url(input.original_url):
        return JSONResponse(status_code=400, content={"message": "Invalid URL!", "short_url": ""})
    response, short_url = insert_url(input.original_url, input.short_url)
    return JSONResponse(status_code=response.value["code"], content={"message": response.value["message"], 
        "short_url": short_url})

#API Endpoint for getting count of URL
@app.get("/url/count/")
async def get_url_count(short_url: str):
    return JSONResponse(status_code=200, content={"count": str(get_counter(short_url))})

def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
