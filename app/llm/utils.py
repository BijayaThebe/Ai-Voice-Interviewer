import re

def sanitize_input(text: str) -> str:
    """Remove problematic characters to avoid prompt corruption."""
    return re.sub(r'[<>"{}]', '', text.strip())[:500]