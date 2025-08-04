import base64
from pathlib import Path

def get_logo_base64():
    """Convert the Guinness logo to base64 for embedding in HTML"""
    try:
        logo_path = Path("guinness_logo.png")
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                data = f.read()
                return base64.b64encode(data).decode()
        return None
    except Exception as e:
        print(f"Error encoding logo: {e}")
        return None