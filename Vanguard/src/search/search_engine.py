"""
The Vanguard Wikipedia API Search Engine System
"""

import os, re
from collections import defaultdict

_DATA_PATH = r"C:\\Users\\Administrator\\.vscode\\durendal\\Vanguard\\data"

# ====================================================== #
# NOTE THIS IS NOT COMPATIBLE WITH THE ARTICLE()-SYSTEM! #
# ====================================================== #

def build_index(directory_path):
    inverted_index = defaultdict(set)
    word_regex = re.compile(r'\b\w+\b')
    filename: str
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                words = word_regex.findall(content)
                for word in words:
                    inverted_index[word].add(filename)
                    
    return inverted_index

search_index = build_index(_DATA_PATH)

def search_keywords(query: str, index: defaultdict):
    query_words = query.lower().split()
    if not query_words:
        return set()
        
    results: set = index.get(query_words[0], set())
    
    for word in query_words[1:]:
        results = results.intersection(index.get(word, set()))
        
    return results


