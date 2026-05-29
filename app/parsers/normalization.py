"""
Text normalization and summarization utilities.

This module provides functions to clean and normalize text fields like
titles and to extract meaningful summaries from raw HTML descriptions.
"""
from bs4 import BeautifulSoup
from typing import Optional

def normalize_title(title: str) -> str:
    """
    Normalize a title string for deduplication.

    Strips leading/trailing whitespace, converts to lowercase, and replaces
    multiple internal spaces with a single space.

    Args:
        title (str): The raw title.

    Returns:
        str: The normalized title.
    """
    if not title:
        return ""
    return ' '.join(title.lower().strip().split())

def extract_deterministic_summary(html_content: Optional[str]) -> str:
    """
    Extract the first meaningful paragraph from HTML content.

    Parses the HTML and attempts to find the first `<p>` tag that contains
    at least 40 characters of text. If found, it truncates the text to 250
    characters. If no such paragraph is found, it falls back to extracting
    all text and truncating it.

    Args:
        html_content (Optional[str]): The raw HTML description.

    Returns:
        str: A plain text summary of up to 250 characters.
    """
    if not html_content:
        return ""
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find the first paragraph that has some length
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 40: # Meaningful length
            # Simple truncation
            if len(text) > 250:
                return text[:247] + "..."
            return text
            
    # Fallback to general text extraction
    text = soup.get_text(separator=' ', strip=True)
    if len(text) > 250:
        return text[:247] + "..."
    return text
