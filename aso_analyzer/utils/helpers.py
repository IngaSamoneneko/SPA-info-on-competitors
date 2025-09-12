def extract_app_id(url: str, platform: str) -> str:
    """Extract app ID from store URL"""
    if platform == "app-store":
        if "id" in url:
            # Handle Apple App Store URLs
            parts = url.split("id")
            if len(parts) > 1:
                app_id = parts[1].split("?")[0].strip(" /")
                return app_id
    else:
        if "id=" in url:
            # Handle Google Play Store URLs
            parts = url.split("id=")
            if len(parts) > 1:
                app_id = parts[1].split("&")[0]
                return app_id
    raise ValueError("Could not extract app ID from URL")