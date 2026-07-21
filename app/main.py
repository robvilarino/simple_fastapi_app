from fastapi import FastAPI, HTTPException
import httpx

def valvelogic(a: str, b: str, op: str) -> dict[str, int]:
    result = eval(f"{a} {op} {b}")
    if result == 3:
        return {"we dont do that here": 69}
    else:
        return {"result": result}

app = FastAPI(
    title="My First FastAPI Application",
    description="A simple FastAPI application",
    version="0.1.0",
)

@app.get("/")
def read_home() -> dict[str, str]:
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/hello/{name}")
def say_name(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}"}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

'''@app.get("/mathvalve/add/{a}/{b}")
def add_numbers(a: int, b: int) -> dict[str, int]:
    return valvelogic(str(a), str(b), "+")'''

@app.get("/mathvalve/{op}/{a}/{b}")
def evaluate_operation(a: int, b: int, op: str) -> dict[str, int]:
    op_dict = {
        "add": "+",
        "subtract": "-",
        "multiply": "*",
        "divide": "/"
    }
    if op in op_dict:
        return valvelogic(str(a), str(b), op_dict[op])
    else:
        return {"error": "Invalid operation"}
    
@app.get("/randombibleverse")
def get_random_bible_verse() -> str:
    
    url = "https://bible-api.com/data/web/random"
    response = httpx.get(url)
    
    if response.status_code == 200:
        verse_data = response.json()
        
        text = verse_data["random_verse"]["text"]
        book = verse_data["random_verse"]["book"]
        chapter = verse_data["random_verse"]["chapter"]
        verse = verse_data["random_verse"]["verse"]
        translation = verse_data["translation"]["name"]
        
        return f'{text} - {book} {chapter}:{verse} ({translation})'
    
@app.get("/hitmetubbs")
def hit_me_tubbs() -> dict[str, str]:
    url = "https://miamivice.fandom.com/api.php"

    params = {
    "action": "query",
    "format": "json",
    "formatversion": 2,

    "generator": "random",
    "grnnamespace": 0,
    "grnlimit": 1,
    
    "prop": "revisions|info",
    "rvprop": "content",
    "rvslots": "main",
    "inprop": "url",
    }

    try:
        response = httpx.get(
            url,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Could not connect to the Miami Vice Wiki",
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502,
            detail="The Miami Vice Wiki returned an error",
        )

    tubbs_report = response.json()
    pages = tubbs_report.get("query", {}).get("pages", [])

    if not pages:
        raise HTTPException(
            status_code=502,
            detail="The Miami Vice Wiki returned no articles",
        )
    
    article = pages[0]

    summary = article.get("revisions", [{}])[0].get("slots", {}).get("main", {}).get("content") or "No summary available."
    print(summary)

    return {
        "title": article["title"],
        "summary": summary,
        "url": article["fullurl"],
    }