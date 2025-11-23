import socket

def shopify_subdomain_available(store_name: str) -> bool:
    """
    Returns True if storename.myshopify.com does NOT resolve,
    meaning it is available.
    """
    domain = f"{store_name.lower()}.myshopify.com"

    try:
        socket.gethostbyname(domain)
        # If resolved → domain is taken
        return False
    except socket.gaierror:
        # If not resolved → available
        return True
