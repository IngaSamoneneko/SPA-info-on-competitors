import os
import httpx
from typing import Optional, Dict, List
from schemas.models import AppInfo, KeywordData, AppAnalysis
from fastapi import HTTPException

class ASOService:
    def __init__(self):
        self.rapidapi_key = "cee1e1d23amshf0f29de25567e94p1bf646jsn90e342a0853a"  # Your new key
        self.rapidapi_host = "app-store-and-google-play-api.p.rapidapi.com"
        self.base_url = f"https://{self.rapidapi_host}"




    async def search_apps(self, query: str, platform: str, country: str = "us", language: str = "en") -> List[AppInfo]:
        endpoint = f"v1/{platform}/search"  # Verified endpoint structure
        
        params = {
            "country": country,
            "language": language,
        }
        if platform == 'app-store':
            params['term'] = query
        else:
            params['text'] = query

        data = await self._make_request(endpoint, params)
        return self._parse_search_results(data.get("results", []), platform)

    async def _make_request(self, endpoint: str, params: dict) -> dict:
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": self.rapidapi_host
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient() as client:
                # Using GET with query parameters
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"API request failed: {str(e)}"
            )





    async def get_competitors(self, app_id: str, platform: str, country: str = "us", limit: int = 5) -> List[AppInfo]:
        endpoint = f"v1/{platform}/similar"
        params = {
            "id": app_id,
            "country": country,
            "language": "en"
        }
        
        data = await self._make_request(endpoint, params)
        return self._parse_search_results(data.get("results", [])[:limit], platform)

    async def get_keywords(self, app_id: str, platform: str, country: str = "us") -> List[KeywordData]:
        endpoint = f"v1/{platform}/keywords"
        params = {
            "id": app_id,
            "country": country,
            "language": "en"
        }
        
        data = await self._make_request(endpoint, params)
        return self._parse_keywords(data.get("keywords", []))

    def _parse_search_results(self, results: List[Dict], platform: str) -> List[AppInfo]:
        return [
            AppInfo(
                app_id=str(app["trackId"] if platform == "app-store" else app["appId"]),
                name=app["trackName"] if platform == "app-store" else app["title"],
                platform=platform,
                icon_url=app["artworkUrl100"] if platform == "app-store" else app["icon"],
                developer=app.get("artistName"),
                rating=app.get("averageUserRating"),
                store_url=app.get("trackViewUrl") if platform == "app-store" else app.get("url")
            )
            for app in results
        ]

    def _parse_app_details(self, data: Dict, platform: str, app_id: str) -> AppInfo:
        return AppInfo(
            app_id=app_id,
            name=data.get("trackName") if platform == "app-store" else data.get("title"),
            platform=platform,
            icon_url=data.get("artworkUrl512") if platform == "app-store" else data.get("icon"),
            developer=data.get("artistName"),
            rating=data.get("averageUserRating"),
            store_url=data.get("trackViewUrl") if platform == "app-store" else data.get("url")
        )

    def _parse_keywords(self, keywords: List[Dict]) -> List[KeywordData]:
        return [
            KeywordData(
                keyword=kw["keyword"],
                position=kw["position"],
                volume=kw.get("volume"),
                traffic=kw.get("traffic")
            )
            for kw in keywords
        ]