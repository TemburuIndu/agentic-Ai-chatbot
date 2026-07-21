# utils.py
import re

def contains_api_or_url(text: str) -> bool:
    """
    Returns True if the text contains interactive API documentation patterns.
    """
    # REST API endpoint patterns with HTTP methods
    api_endpoint_pattern = re.compile(
        r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+https?://', re.IGNORECASE
    )
    
    # Instructional API patterns
    instructional_patterns = [
        r'\bcall\s+this\s+endpoint',
        r'\bcall\s+the\s+api',
        r'\bmake\s+a\s+request\s+to',
        r'\bendpoint\s+to\s+get',
        r'\bapi\s+response',
        r'\b(GET|POST|PUT|DELETE|PATCH)\s+https?://',
        r'\bcurl\s+-[XH]',
        r'\b(request|response)\s*(body|payload|headers?)',
        r'\b(authorization|auth)\s*:\s*(bearer|basic|api[_-]?key)',
        r'\bapi[_-]?key\s*[:=]',
        r'\b(query\s*param|path\s*param|header\s*param)',
        r'\b(endpoint|api)\s*:\s*https?://',
        r'\b(base\s*url|baseurl)\s*:\s*https?://',
        r'\b(content-type|accept)\s*:\s*application/',
        r'\b(status\s*code|http\s*status)\s*:\s*\d{3}',
    ]
    
    # Check for any instructional API pattern
    for pattern in instructional_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False

