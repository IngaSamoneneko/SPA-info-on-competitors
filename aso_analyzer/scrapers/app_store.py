from typing import Dict  # Add this line at the very top
import requests
from bs4 import BeautifulSoup

def scrape_app_store(app_url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(app_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Debug: Save HTML for inspection
        with open("debug_app_page.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        # ---- 1. MAIN APP DATA ----
        name = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
        developer = soup.find("h2").get_text(strip=True) if soup.find("h2") else None
        
        # ---- 2. COMPETITOR SCRAPING ----
        competitors = []
        
        similar_sections = [
            soup.find("div", {"data-test-we-lockup": True}),  # New selector
            soup.find("div", class_="l-row l-row--peek"),     # Old selector
            soup.find("div", class_="we-similar-apps")        # Alternative
        ]
        
        for section in similar_sections:
            if section:
                apps = section.find_all("a", href=True)
                for app in apps[:5]:  # Limit to top 5
                    app_name = app.find("h3").get_text(strip=True) if app.find("h3") else "Unknown"
                    app_url = "https://apps.apple.com" + app["href"] if app["href"].startswith("/") else app["href"]
                    competitors.append({
                        "name": app_name,
                        "url": app_url
                    })
                break  # Use first matching section

        return {
            "name": name,
            "developer": developer,
            "competitors": competitors,
            "scraped_url": app_url,
            "html_saved": "debug_app_page.html",  # For debugging
            "error": None if competitors else "No competitors found (check debug_app_page.html)"
        }

    except Exception as e:
        return {
            "error": f"Scraping failed: {str(e)}",
            "competitors": [],
            "scraped_url": app_url
        }