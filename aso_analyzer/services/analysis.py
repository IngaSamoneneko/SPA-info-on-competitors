import asyncio
from typing import List
from schemas.models import AppAnalysis, CompetitorAnalysis
from services.aso_service import ASOService

aso_service = ASOService()

class AnalysisService:
    async def analyze_app(self, app_id: str, platform: str, country: str = "us") -> AppAnalysis:
        """Analyze a single app's keywords and performance"""
        app_info = await aso_service.get_app_details(app_id, platform, country)
        keywords = await aso_service.get_keywords(app_id, platform, country)
        
        estimated_traffic = sum(
            kw.traffic or (1000 / kw.position) if kw.position <= 10 else 0
            for kw in keywords
        )
        
        return AppAnalysis(
            app_info=app_info,
            total_keywords=len(keywords),
            top_keywords=sorted(keywords, key=lambda x: x.position)[:10],
            estimated_traffic=estimated_traffic
        )

    async def competitive_analysis(self, app_id: str, platform: str, country: str = "us") -> CompetitorAnalysis:
        """Perform full competitive analysis"""
        # Analyze main app
        main_analysis = await self.analyze_app(app_id, platform, country)
        
        # Get and analyze competitors
        competitors = await aso_service.get_competitors(app_id, platform, country)
        
        competitor_tasks = [
            self.analyze_app(comp.app_id, platform, country)
            for comp in competitors
        ]
        competitor_analyses = await asyncio.gather(*competitor_tasks)
        
        # Calculate metrics
        total_keywords = [a.total_keywords for a in competitor_analyses]
        avg_keywords = sum(total_keywords) / len(total_keywords) if total_keywords else 0
        max_keywords = max(total_keywords) if total_keywords else 0
        
        competitor_traffic = [a.estimated_traffic for a in competitor_analyses]
        avg_traffic = sum(competitor_traffic) / len(competitor_traffic) if competitor_traffic else 0
        traffic_diff = avg_traffic - main_analysis.estimated_traffic
        
        return CompetitorAnalysis(
            main_app=main_analysis,
            competitors=competitor_analyses,
            average_keywords=avg_keywords,
            max_keywords=max_keywords,
            traffic_difference=traffic_diff
        )