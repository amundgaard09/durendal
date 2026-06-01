
from modules.page_ir import PageIR
from pathlib import Path
from wikipediaapi import WikipediaPage, WikipediaPageSection
from awpc.src.unipy.uniCLI import console_print

def _render_sections(sections: list[WikipediaPageSection], level: str = 2) -> str:
    console_print("RENDERER", "BLUE", "Rendering sections into Markdown...", "green")
    markdown = ""
    for sec in sections:
        markdown += f"{'#' * level} {sec.title}\n\n"
        markdown += sec.text + "\n\n"

        if sec.sections:
            markdown += _render_sections(sec.sections, level + 1)

    return "\n" + markdown

def preprocess_to_page_ir(page: WikipediaPage) -> PageIR:
    console_print("IR PREPROCESSOR", "BLUE", "Preprocessing page to PageIR...", "green")
    return PageIR(
        title=page.title,
        summary=page.summary,
        text=page.text,
        links=[],
        headings=[],
        sections=page.sections
    )
    
def extract_links(ir: PageIR, page: WikipediaPage) -> PageIR:
    console_print("LINK EXTRACTOR", "BLUE", "Extracting links...", "green")

    ir.links = list(page.links.keys())
    return ir

def extract_headings(ir: PageIR) -> PageIR:
    console_print("HEADING EXTRACTOR", "BLUE", "Extracting headings...", "green")

    lines = ir.summary.split("\n")
    ir.headings = [line for line in lines if line.strip().isupper()]

    return ir

def format_page(ir: PageIR) -> str:
    md = f"# {ir.title}\n\n"

    md += "## Summary\n"
    md += ir.summary + "\n\n"

    md += "## Content\n"
    md += _render_sections(ir.sections) + "\n\n"

    return md

def insert_links(text: str, links: list[str]) -> str:
    console_print("LINK INSERTER", "BLUE", "Inserting links into Markdown document...", "green")
    link_set = set(links)
    seen = set()

    words = text.split()
    result = []

    for w in words:
        clean = w.strip(".,()[]")

        if clean in link_set and clean not in seen:
            result.append(f"[[{clean}]]")
            seen.add(clean)
        else:
            result.append(w)

    return " ".join(result)
    
def save_markdown(name: str, content: str, path: Path) -> None:
    console_print("MARKDOWN SAVER", "BLUE", f"Saving Markdown to {path}...", "green")
    """Saves the given Markdown content to the specified path."""
    full_path = path / f"{name}.md"
    full_path.write_text(content, encoding="utf-8")

def main(name: str, page: WikipediaPage, path: Path) -> str:
    """
    The Markdown Compiler (MDC) 
    
    MDC takes a Wikipedia page and compiles it into a structured Markdown document. 
    It processes the page to extract the title, summary, links, and headings, formats this information into Markdown, and saves it to the specified path.
    """
    ir = preprocess_to_page_ir(page)
    ir = extract_links(ir, page)
    ir = extract_headings(ir)
    markdown = format_page(ir)
    markdown = insert_links(markdown, ir.links)

    save_markdown(name, markdown, path)

    return markdown

    
    