
from wikipediaapi import WikipediaPageSection
from dataclasses import dataclass

@dataclass
class PageIR:
    """
    Page Intermediate Representation (PageIR) is a structured representation of a Wikipedia page's content to help streamline the Markdown compilation process.
    """
    title: str
    summary: str
    text: str 
    links: list[tuple[str, str]]
    headings: list[str]
    sections: list[WikipediaPageSection]