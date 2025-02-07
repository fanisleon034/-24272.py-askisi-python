from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import uvicorn

app = FastAPI()

def load_quotes():
    
 
    try:
        with open("quotes.json", "r", encoding="utf-8") as f:
            quotes = json.load(f)
        return quotes
    except Exception as e:
        print("Σφάλμα φόρτωσης του quotes.json:", e)
        return []

@app.get("/quotes")
def get_quotes(author: str = None):
 
    quotes = load_quotes()
    if author:
        filtered = [quote for quote in quotes if quote.get("author", "").lower() == author.lower()]
        return JSONResponse(content=filtered)
    else:
        return JSONResponse(content=quotes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

