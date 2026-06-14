from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
from linkformat import clean_link

app = FastAPI()

class URLRequest(BaseModel):
    url: str

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; md-link-fetcher/1.0)"
}
@app.post("/api/fetch")
async def fetch_title(req: URLRequest):
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10, verify="/etc/ssl/certs/ca-certificates.crt") as client:
            resp = await client.get(req.url, headers=HEADERS)
            resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Parse the HTML, turn into object soup.
    soup = BeautifulSoup(resp.text, "lxml")
    
    # Collapse whitespace (some titles have \n\t in them)
    title = soup.title.string.strip() if soup.title else req.url
    title = " ".join(title.split())
    
    # Remove [] from titles
    title = title.replace("[", "").replace("]", "")
    
    # Add a Discodr Version
    markdown = f"[{title}]({req.url})"
    discord = f"[{title}](<{req.url}>)"

    # Clean URL-as-text version (scheme + .html trimmed off the label)
    clean = clean_link(req.url)

    return {"markdown": markdown, "discord": discord, "clean": clean}

# Serve the frontend last (catch-all)
app.mount("/", StaticFiles(directory="static", html=True), name="static")