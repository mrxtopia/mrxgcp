import uuid
import sys
import urllib.parse

def generate_vless_link(run_url, user_uuid=None, name="MRX_Safari"):
    """
    Generates a VLESS link for a specific Google Cloud Run URL.
    """
    if not user_uuid:
        user_uuid = str(uuid.uuid4())
    
    # Clean up the URL (remove https:// if present)
    host = run_url.replace("https://", "").replace("http://", "").strip("/")
    
    # Parameters based on the user's example
    params = {
        "path": "/",
        "security": "tls",
        "alpn": "h3,h2,http/1.1",
        "encryption": "none",
        "insecure": "1",
        "host": host,
        "fp": "chrome",
        "type": "ws",
        "allowInsecure": "1",
        "sni": "api.safaricom.et"
    }
    
    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    
    # The example uses google.com:443 as the connection target, probably for masking or CDN
    # while the real host is in the 'host' parameter.
    vless_link = f"vless://{user_uuid}@google.com:443?{query_string}#{name}"
    
    return vless_link, user_uuid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_vless.py <cloud_run_url> [uuid]")
        sys.exit(1)
        
    url = sys.argv[1]
    provided_uuid = sys.argv[2] if len(sys.argv) > 2 else None
    
    link, generated_uuid = generate_vless_link(url, provided_uuid)
    
    print("-" * 30)
    print(f"Generated UUID: {generated_uuid}")
    print(f"VLESS Link:")
    print(link)
    print("-" * 30)
