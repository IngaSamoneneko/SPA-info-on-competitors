from pydantic import BaseModel
from typing import Optional, List

class AppInfo(BaseModel):
    app_id: str
    name: str
    platform: str  # 'app-store' or 'google-play'
    icon_url: Optional[str] = None
    developer: Optional[str] = None
    rating: Optional[float] = None
    store_url: Optional[str] = None

class KeywordData(BaseModel):
    keyword: str
    position: int
    volume: Optional[int] = None
    traffic: Optional[float] = None

class AppAnalysis(BaseModel):
    app_info: AppInfo
    total_keywords: int
    top_keywords: List[KeywordData]
    estimated_traffic: float

class CompetitorAnalysis(BaseModel):
    main_app: AppAnalysis
    competitors: List[AppAnalysis]
    average_keywords: float
    max_keywords: int
    traffic_difference: float