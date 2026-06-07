"""
The Vanguard Wikipedia API Pagefinder system. 

This file (or more precisesly a script) finds the wikipedia page for the query, and saves the entire page to a Markdown file.
"""

import json, datetime

from hashlib import sha256
from pathlib import Path
from typing import Any
from wikipediaapi import Wikipedia, WikipediaPage
from modules.article import Article
from modules.metadata import Metadata
from md_compiler.compiler.main import main as md_compile
from durapy import uniCLI

_ARTICLE_JSON_DIR = r"C:\\Users\\Administrator\\.vscode\\durendal\\Vanguard\\data\\articles"
_MARKDOWN_DIR = r"C:\\Users\\Administrator\\.vscode\\durendal\\Vanguard\\data\\markdown"
_TEMPLATE_DIR = r"C:\\Users\\Administrator\\.vscode\\durendal\\Vanguard\\data\\templates"

def insert_json(path_to_json: str, content_dict: dict) -> bool:
    """Inserts a dictionary into a `JSON` file. If the file does not exist, it creates it."""
    
    try:
        with open(path_to_json, "w", encoding="utf-8") as JSONFile:
            json.dump(content_dict, JSONFile, indent=4, sort_keys=True)
    except Exception as e:
        uniCLI.console_print("JSON Writer", "white", f"Error writing to JSON file: {e}", "red")
        return False
    uniCLI.console_print("JSON Writer", "white", f"Successfully wrote to JSON file: {path_to_json}", "green")
    return True

def get_wiki(_user_agent: str, _language: str = "en") -> Wikipedia:
    return Wikipedia(user_agent=_user_agent, language=_language)
def get_page(query: str, _wiki: Wikipedia) -> WikipediaPage:
    page = _wiki.page(query)
    return page
def get_source(source: Any) -> str:
    if isinstance(source, WikipediaPage):
        return "Wikipedia"  
def parse(query: str) -> str:
    return query.strip().replace(" ", "_")

def main(page: WikipediaPage) -> None:
    """
    The Pagefinder Main Function
    
    The Pagefinder is responsible for finding the Wikipedia page for the given query, and saving the entire page to a Markdown file. 
    It also creates an `Article` object for the page, and saves it as a JSON file for later retrieval and indexing.
    """  
    
    if page.exists():
        content, title = page.text, page.title
        uniCLI.console_print("PAGEFINDER", "white", f"Found Wikipedia page: {title}", "green")
    
    else:
        uniCLI.console_print("PAGEFINDER", "white", "No Wikipedia page found.", "red")
        return
    
    try:
        jsonpath = (_ARTICLE_JSON_DIR + "\\" + parse(title) + ".json").lower()
        mdpath = (_MARKDOWN_DIR + "\\" + parse(title) + ".md").lower()
            
        article = Article(
                name=title, 
                idstr=sha256(title.encode()).hexdigest(), 
                title=parse(title), 
                contentpath=Path(mdpath), 
                links=[], 
                metadata = Metadata(
                    source     = get_source(page),
                    url        = page.fullurl,
                    word_count = len(content.split()),
                    saved_at   = datetime.datetime.now().isoformat(),
                    link_count = len(page.links),
                    language   = page.language
                )
            )

        md_compile(title, page, Path(_MARKDOWN_DIR))
        insert_json(jsonpath, article.to_dict())
        uniCLI.console_print("PAGEFINDER", "white", "Successful save and article creation!", "green")
            
    except FileExistsError:
        uniCLI.console_print("PAGEFINDER", "white", "File already exists! Use the search engine instead", "red")
    except Exception as e:
        uniCLI.console_print("PAGEFINDER", "white", f"An error occurred: \n {e}", "red")