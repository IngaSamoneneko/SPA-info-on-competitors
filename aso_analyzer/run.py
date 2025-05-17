from dotenv import load_dotenv
from pathlib import Path
import os
import uvicorn

# Load environment first
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Verify
print("Environment Variables Loaded:")
print(f"RAPIDAPI_KEY exists: {bool(os.getenv('RAPIDAPI_KEY'))}")

# Import and run app
from main import app

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)