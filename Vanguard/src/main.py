
from search.pagefinder import get_page, get_wiki, parse, main as pagefinder
from durapy import uniCLI

username = "Simon Stordal Amundgaard"
usermail = "nomispus@icloud.com"

if __name__ == "__main__":
    if not username or not usermail:
        uniCLI.console_print("MAIN", "white", "Username and usermail must be set to use Vanguard!", "red")
        exit(1)
        
    uniCLI.console_print("Vanguard", "white", "Starting Vanguard...", "green")
    uniCLI.console_print("Vanguard", "white", f"Logged in as: {username} ({usermail})", "green")
    
    wiki = get_wiki(f"{username} ({usermail})")
    query = parse(str(uniCLI.console_input("Vanguard", "white", "Article to pull:")))
    page = get_page(query, wiki)

    pagefinder(page)
    
