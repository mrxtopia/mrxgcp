import uuid
import sys
import urllib.parse

def generate_vless_link(run_url, user_uuid=None, name="MRX_Safari", path="/mrx-vless"):
    """
    Generates a VLESS link for a specific Google Cloud Run URL.
    """
    if not user_uuid:
        user_uuid = str(uuid.uuid4())
    
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
    
    return vless_link, user_uuid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_vless.py <cloud_run_url> [count]")
        sys.exit(1)
        
    url = sys.argv[1]
    count = 1
    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except ValueError:
            pass # Use default count of 1
    
    print("-" * 30)
    print(f"Generating {count} VLESS link(s)...")
    print("-" * 30)
    
    all_uuids = []
    for i in range(count):
        link, gen_uuid = generate_vless_link(url, name=f"MRX_Safari_{i+1}")
        all_uuids.append(gen_uuid)
        print(f"--- User {i+1} ---")
        print(f"UUID: {gen_uuid}")
        print(f"Link: {link}\n")
    
    print("-" * 30)
    print("TIP: To use these specific UUIDs on Cloud Run, set this environment variable:")
    print(f'UUIDS={",".join(all_uuids)}')
    print("-" * 30)
