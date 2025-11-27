import socket
import re
from typing import Optional

def shopify_subdomain_available(store_name: str) -> bool:
    """
    Checks the DNS resolution for a potential Shopify subdomain.
    Returns True if storename.myshopify.com does NOT resolve (is available).
    """
    if not store_name or not isinstance(store_name, str):
        return False

    # 1. Slugify the name (required for proper Shopify subdomain format)
    slugified_name = store_name.lower()
    slugified_name = re.sub(r'[^\w]+', '-', slugified_name)
    slugified_name = slugified_name.strip('-_')

    if not slugified_name:
        return False
        
    domain = f"{slugified_name}.myshopify.com"

    try:
        # Set a short timeout (e.g., 2 seconds) for the DNS query
        socket.setdefaulttimeout(2) 
        
        # If resolved successfully, the domain is taken (not available)
        socket.gethostbyname(domain)
        return False
    except (socket.gaierror, socket.timeout):
        # If gaierror (name not found) or timeout, the domain is likely available
        return True
    except Exception as e:
        # Unexpected server-side error during check. Safest to assume unavailable/failed.
        print(f"Unexpected error during domain check for {domain}: {e}")
        return False