import json
import requests
from urllib.parse import unquote

def handler(request):
    try:
        # Get the target URL from query parameters
        target_url = request.GET.get("url")
        if not target_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
            }

        target_url = unquote(target_url)
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(target_url, headers=headers, timeout=10)

        return {
            "statusCode": resp.status_code,
            "body": resp.text,
            "headers": {
                "Content-Type": resp.headers.get("Content-Type", "application/json"),
                "Access-Control-Allow-Origin": "*"
            },
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
        }
