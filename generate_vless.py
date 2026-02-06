import sys
import urllib.parse

# Hardcoded UUIDs matching config.json
FIXED_UUIDS = [
    "4e7a8b1c-d3f2-4b5a-9c6e-7f8a9b0c1d2e",
    "5f8b9c2d-e4a3-5c6b-0d7e-8f9a0b1c2d3e",
    "6a9c0d3e-f5b4-6d7c-1e8f-9a0b1c2d3e4f",
    "7b0d1e4f-06c5-7e8d-2f9a-0b1c2d3e4f5a",
    "8c1e2f5a-17d6-8f9e-3a0b-1c2d3e4f5a6b",
    "9d2f3a6b-28e7-9a0f-4b1c-2d3e4f5a6b7c",
    "0e3a4b7c-39f8-0b1a-5c2d-3e4f5a6b7c8d",
    "1f4b5c8d-4a09-1c2b-6d3e-4f5a6b7c8d9e",
    "2a5c6d9e-5b1a-2d3c-7e4f-5a6b7c8d9e0f",
    "3b6d7e0f-6c2b-3e4d-8f5a-6b7c8d9e0f1a"
]

def generate_vless_link(run_url, user_uuid, name="MRX_Safari", path="/mrx-vless"):
    """
    Generates a VLESS link for a specific Google Cloud Run URL.
    """
    # Clean up the URL (remove https:// if present)
    host = run_url.replace("https://", "").replace("http://", "").strip("/")
    
    # Parameters based on the user's example and our best-practice config
    params = {
        "path": path,
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
    
    # Use google.com:443 for connection target with host override for CDN/WAF bypass
    vless_link = f"vless://{user_uuid}@google.com:443?{query_string}#{name}"
    
    return vless_link

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_vless.py <cloud_run_url> [count]")
        print("Example: python generate_vless.py my-app.run.app 10")
        sys.exit(1)
        
    url = sys.argv[1]
    count = 1
    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except ValueError:
            pass # Use default count of 1
    
    # Limit count to 10
    count = min(count, 10)
    
    print("-" * 30)
    print(f"Generating {count} VLESS link(s) using FIXED UUIDs...")
    print("-" * 30)
    
    for i in range(count):
        user_uuid = FIXED_UUIDS[i]
        link = generate_vless_link(url, user_uuid, name=f"MRX_Safari_{i+1}")
        print(f"--- User {i+1} ---")
        print(f"UUID: {user_uuid}")
        print(f"Link: {link}\n")
    
    print("-" * 30)
    print("DONE: These links match the hardcoded UUIDs in your server config.")
    print("-" * 30)
