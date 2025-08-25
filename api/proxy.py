import json
import requests
from urllib.parse import unquote

def handler(request):
    # Handle CORS preflight for any method
    if request.method == "OPTIONS":
        return {
            "statusCode": 204,
            "body": "",
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",  # Allow all HTTP methods
                "Access-Control-Allow-Headers": "*",  # Allow all headers
            },
        }

    try:
        # Get the target URL from query parameters
        target_url = request.GET.get("url")
        if not target_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "*",
                    "Access-Control-Allow-Headers": "*",
                },
            }

        target_url = unquote(target_url)
        headers = {"User-Agent": "Mozilla/5.0"}

        # Use the same method as the incoming request
        method = request.method.upper()
        data = request.get_data() if method in ["POST", "PUT", "PATCH"] else None

        resp = requests.request(method, target_url, headers=headers, data=data, timeout=10)

        # Return the response with proper CORS headers
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded_headers]

        # Always allow CORS
        response_headers.append(("Access-Control-Allow-Origin", "*"))
        response_headers.append(("Access-Control-Allow-Methods", "*"))
        response_headers.append(("Access-Control-Allow-Headers", "*"))

        return {
            "statusCode": resp.status_code,
            "body": resp.text,
            "headers": dict(response_headers),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
        }
