import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Notion API Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"

# Your Notion IDs (replace with your actual IDs)
GOALS_PAGE_ID = os.getenv("GOALS_PAGE_ID", "your-goals-page-id-here")
TODO_DATABASE_ID = os.getenv("TODO_DATABASE_ID", "your-todo-database-id-here")

# Task generation settings
MAX_TITLE_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 5  # sentences
