"""
URL parsing and canonicalization utilities.

This module provides functions to normalize URLs by removing tracking
parameters and standardizing the format, aiding in accurate deduplication.
"""
import urllib.parse

def canonicalize_url(url: str) -> str:
    """
    Remove tracking params and trailing slashes to form a canonical URL.

    Strips out common tracking query parameters (e.g., utm_*) and removes
    any trailing slashes from the path. Also converts the URL to lowercase.

    Args:
        url (str): The raw URL.

    Returns:
        str: The canonicalized URL.
    """
    if not url:
        return ""
    
    parsed = urllib.parse.urlparse(url)
    
    # Remove tracking query parameters
    query_params = urllib.parse.parse_qsl(parsed.query)
    clean_params = [(k, v) for k, v in query_params if not k.startswith("utm_") and k not in {"ref", "source", "tracking"}]
    
    clean_query = urllib.parse.urlencode(clean_params)
    
    # Remove trailing slash from path
    path = parsed.path
    if path.endswith('/') and len(path) > 1:
        path = path[:-1]
        
    canonical = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        clean_query,
        # Intentionally dropping fragment as it's client side usually, unless needed
        "" 
    ))
    return canonical.lower().strip()
