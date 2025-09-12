import os, requests
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

RAPIDAPI_KEY  = os.getenv("RAPID_KEY" , "cee1e1d23amshf0f29de25567e94p1bf646jsn90e342a0853a")
RAPIDAPI_HOST = "app-store-and-google-play-api.p.rapidapi.com"

app = FastAPI()



# ---------- API ----------

@app.get("/api/search")
def search_apps(query: str,
                platform: str = "google-play",
                country: str = "us",
                language: str = "en",
                limit: int = 5):

    params = {
        "country":  country,
        "language": language,
        "limit":    limit
    }
    if platform == "app-store":
        params["term"] = query
        endpoint = "v1/app-store/search"
    else:
        params["text"] = query
        endpoint = "v1/google-play/search"

    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "X-RapidAPI-Key":  RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    # ⬇️ відлагоджувальні повідомлення ТУТ, усередині функції
    print("🔍 Платформа:", platform)
    print("🔍 Параметри:", params)
    print("🔍 URL:", url)

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print("🔍 Response text:", r.text)          # <— теж тут
        r.raise_for_status()
        api_json = r.json()
        apps = api_json.get("data", {}).get("searched_apps", [])   # для цього API
        return apps
    except requests.HTTPError as e:
        raise HTTPException(status_code=r.status_code,
                            detail=f"RapidAPI error: {r.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health-check
@app.get("/health")
def health(): return JSONResponse({"ok": True})


# ⬇️ буде віддавати / (index.html)
app.mount("/",
          StaticFiles(directory="templates", html=True),
          name="static")

