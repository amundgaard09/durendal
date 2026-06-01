
from wikipediaapi import WikipediaPage
from search.pagefinder import get_page, get_wiki, parse, main 

if __name__ == "__main__":
    wiki = get_wiki("Simon Stordal Amundgaard (nomispus@icloud.com)")
    query = parse(str(input("Enter Query: ")))
    page = get_page(query, wiki)

    main(page)
    
