
import re as regex

from modules.page_ir import PageIR
from pathlib import Path
from wikipediaapi import WikipediaPage, WikipediaPageSection
from durapy import uniCLI

### MCD Enhancement proposals:
### 1. Use an LLM API (e.g. OpenAI) to clean up the article (e.g. make links at the See Also section actual links.)

def check_if_article_exists(name: str, path: Path) -> bool:
    """Checks if an article with the given name already exists in the specified path."""
    full_path = path / f"{name}.md"
    exists = full_path.exists()
    
    uniCLI.console_print("ARTICLE CHECKER", "white", f"Article '{name}' exists: {exists}", "green" if exists else "red")
    
    return exists

def render_sections(sections: list[WikipediaPageSection], level: int = 2) -> str:
    uniCLI.console_print("RENDERER", "blue", "Rendering sections into Markdown...", "green")
    markdown = ""
    for sec in sections:
        markdown += f"{'#' * level} {sec.title}\n\n"
        markdown += sec.text + "\n\n"

        if sec.sections:
            markdown += render_sections(sec.sections, level + 1)

    return "\n" + markdown

def preprocess_to_page_ir(page: WikipediaPage) -> PageIR:
    """
    Preprocesses the Wikipedia page into a `PageIR`, which is an intermediate representation of the page that contains the title, summary, text, links, headings, and sections. 
    
    This will be used for further processing and formatting into Markdown.
    """
    
    uniCLI.console_print("IR PREPROCESSOR", "white", "Preprocessing page to PageIR...", "green")
    
    return PageIR(
        title=page.title,
        summary=page.summary,
        raw_text=page.text,
        markdown_text="",
        links=[],
        headings=[],
        sections=page.sections
    )
    
def extract_links(ir: PageIR, page: WikipediaPage) -> PageIR:
    """Extracts links from the page and adds them to the PageIR."""
    uniCLI.console_print("LINK EXTRACTOR", "white", "Extracting links...", "green")

    ir.links = list(page.links.keys())
    return ir

def extract_headings(ir: PageIR) -> PageIR:
    """Extracts headings from the page summary and sections."""
    uniCLI.console_print("HEADING EXTRACTOR", "white", "Extracting headings...", "green")

    lines = ir.summary.split("\n")
    ir.headings = [line for line in lines if line.strip().isupper()]

    return ir

def format_page(ir: PageIR) -> str:
    """Formats the PageIR into a Markdown string."""
    uniCLI.console_print("MD FORMATTER", "white", "Formatting page into Markdown...", "green")
    md = f"# {ir.title}\n\n"

    md += "## Summary\n"
    md += ir.summary + "\n\n"

    md += render_sections(ir.sections) + "\n\n"

    return md

def inject_wikilinks(IR: PageIR) -> str:
    """Injects wikilinks into the Markdown text by wrapping link terms in double square brackets. This is a simple heuristic that may not be perfect, but it attempts to identify linkable terms and mark them for later processing."""
    
    uniCLI.console_print("LINK INJECTOR", "white", "Injecting wikilinks into Markdown document...", "green")
    
    text = IR.markdown_text
    
    link_set = set(IR.links)
    seen = set()

    tokens = regex.split(r'(\s+)', text)
    result = []

    for token in tokens:
        if token.isspace() or token == "":
            result.append(token)
            continue

        leading = len(token) - len(token.lstrip(".,()[]"))
        trailing = len(token) - len(token.rstrip(".,()[]"))
        prefix = token[:leading]
        suffix = token[len(token) - trailing:]
        core = token[leading: len(token) - trailing] if trailing else token[leading:]

        if core in link_set and core not in seen:
            result.append(f"{prefix}[[{core}]]{suffix}")
            seen.add(core)
        else:
            result.append(token)

    return "".join(result)

def split_into_sections(IR: PageIR) -> str:
    """
    Restore Markdown section structure after link injection.
    If whitespace is preserved by inject_wikilinks, this will leave the text unchanged.
    """
    
    text = IR.markdown_text

    uniCLI.console_print("SECTION SPLITTER", "white", "Splitting text into sections...", "green")
    
    if "\n" in text:
        return text

    # If the text was flattened into a single line, restore heading boundaries.
    text = regex.sub(r'\s+(?=#+\s)', '\n\n', text)
    return text

def save_markdown(IR: PageIR, name: str, path: Path) -> None:
    """
    Saves the given Markdown content to a file named `{name}.md` in the specified path. If the file already exists, it will ask the user if they want to overwrite or not.
    """
    uniCLI.console_print("MD SAVER", "white", f"Saving Markdown to {path}...", "green")
    """Saves the given Markdown content to the specified path."""
    full_path = path / f"{name}.md"
    
    if full_path.exists():
        continue_ = uniCLI.console_confirm("MD SAVER", "white", f"Warning: File '{full_path}' already exists and will be overwritten. Overwrite? (y/n)", "yellow")
        if not continue_:
            uniCLI.console_print("MD SAVER", "red", "Operation cancelled.", "red")
            return
        else:
            uniCLI.console_print("MD SAVER", "white", "Proceeding...", "green")
    
    full_path.write_text(IR.markdown_text, encoding="utf-8")

def main(name: str, page: WikipediaPage, path: Path) -> None:
    """
    The Markdown Compiler Pipeline (MDC) 
    
    MDC takes a Wikipedia page and compiles it into a structured Markdown document. 
    It processes the page to extract the title, summary, links, and headings, formats this information into Markdown, and saves it to the specified path.
    """
    
    uniCLI.console_print("MDC PIPELINE", "white", "MDC Pipeline initialized... ", "green")
    
    IR = preprocess_to_page_ir(page)
    IR = extract_links(IR, page)
    IR = extract_headings(IR)
    IR.markdown_text = format_page(IR)
    IR.markdown_text = inject_wikilinks(IR)
    IR.markdown_text = split_into_sections(IR)
    
    save_markdown(IR, name, path)
    
    uniCLI.console_print("MDC PIPELINE", "white", "MDC Pipeline finished... ", "green")
    

    