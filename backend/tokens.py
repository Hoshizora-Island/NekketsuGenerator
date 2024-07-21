from dotenv import load_dotenv
import os
load_dotenv()

def getToken(key: str) -> str:
    return os.getenv(key)