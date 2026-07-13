from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("GROQ exists:", GROQ_API_KEY is not None)

DB_NAME = "data/studygenie.db"

