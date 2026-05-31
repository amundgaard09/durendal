
from pathlib import Path
import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    user_agent="Simon Stordal Amundgaard (nomispus@icloud.com)",
    language="en"
)

page = wiki.page("Python_(programming_language)")

if page.exists():
    print(f"Title: {page.title}")
    print(f"Summary: {page.summary[:200]}...")

