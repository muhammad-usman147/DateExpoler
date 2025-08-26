from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel 
import requests
import re
from typing import Optional, List 
import uvicorn 
import os 

app = FastAPI()

#To mount static files
app.mount("/static", StaticFiles(directory = 'static'),
name = 'static')


class FacebookLinkRequest(BaseModel):
    url: str 

class FacebookInfo(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None 
    image: Optional[str] = None 
    followers: Optional[str] = None 
    verified: Optional[bool] = None 
    error: Optional[str] = None 

class extract_facebook_info(url: str) -> FacebookInfo:
    """ Extract public informatiom from a facebook page """\
    try:
        if not re.match(r'https?://(www\.)?(facebook\.com|fb\.com)/.+', url):
            return FacebookInfo(error = "Invalid Facebook URL")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status() 
        html_content = response.text 

        #extracting basic info using regex (limited due to Facebook's content) 
        title_match = re.search(r'<title[^>]*>([^<]+)</title>',  html_content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Facebook Page"
        
        desc_match = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']',
                               html_content, re.IGNORECASE)
        description = desc.match.group(1) if desc_match else "No description available"

        #extract followers count (limited due to API)
        follower_patterns = [
            r'(\d+(?:,\d+)*)\s+(?:followers?|likes?)',
            r'(\d+\.?\d*[KMB]?)\s+(?:followers?|likes?)'
        ]
        followers = None 
        for pattern in follower_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE) 
            if match:
                followers = match.group(1)
                break 

        return FacebookInfo(
            title = title, 
            description = description, 
            image = image, 
            followers = followers,
            verified = verified
        )

    except requests.RequestException as e:
        return FacebookInfo(error = f"Error fetching data: {str(e)}")
    except Exception as e:
        return FacebookInfo(error = f"Error processing data: {str(e)}")

@app.get('/',response_class = HTMLResponse)
async def read_index():
    """ serve the main HTML page """ 
    try:
        with open('static/index.html', 'r',encoding = 'utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content = html_content)

    except FileNotFoundError:
        return HTMLResponse(content = " <h1> Error: File not Found </h1>", status_code = 404)

@app.post("/extract-facebook-info")
async def extract_facebook_info_endpoint(request: FacebookLinkRequest):
    ''' Extract facebook Page information '''
    info = extract_facebook_info(request.url)
    return info 


if __name__ == "__main__":
    if not os.path.exists('static'):
        os.mkdir("static")

    uvicorn.run(app, host = '0.0.0.0', post= 8000)
