"""
Deterministic tagging module.

This module automatically assigns categories (tags) to opportunities based
on predefined keyword matching against the text content.
"""
import re
from typing import List

KEYWORDS = {
    "ai": ["machine learning", "artificial intelligence", "deep learning", "neural networks", " ai "],
    "robotics": ["robotics", "autonomous systems"],
    "conference": ["call for papers", "cfp", "conference", "symposium"],
    "grant": ["grant", "funding", "scholarship", "fellowship", "award"],
    "undergraduate": ["undergraduate", "bachelor", "ug"],
    "postgraduate": ["postgraduate", "master", "phd", "pg", "doctoral"],
    "cybersecurity": ["cybersecurity", "security", "cryptography"],
}

def extract_deterministic_tags(text: str) -> List[str]:
    """
    Extract tags based on keyword dictionaries and regular expressions.

    Scans the input text for predefined keywords. If a keyword is found
    as a whole word, its corresponding tag category is added to the result.

    Args:
        text (str): The text to analyze (typically title + description).

    Returns:
        List[str]: A list of unique tags found in the text.
    """
    if not text:
        return []
        
    text_lower = text.lower()
    tags = set()
    
    for tag, keywords in KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                tags.add(tag)
                break
                
    return list(tags)
