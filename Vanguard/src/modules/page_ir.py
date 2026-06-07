
from wikipediaapi import WikipediaPageSection
from dataclasses import dataclass

@dataclass
class PageIR:
    """
    Page Intermediate Representation (PageIR) is a structured representation of a Wikipedia page's content to help streamline the Markdown compilation process.
    """
    title: str
    """The title of the Wikipedia page."""
    summary: str
    """A brief summary of the Wikipedia page."""
    raw_text: str
    """The main content of the Wikipedia page."""
    markdown_text: str
    """The Markdown-formatted text of the Wikipedia page, which will be generated from the raw text."""
    links: list[str]
    """A list of strings found in the Wikipedia page."""
    headings: list[str]
    """A list of headings in the Wikipedia page."""
    sections: list[WikipediaPageSection]
    """A list of sections in the Wikipedia page."""