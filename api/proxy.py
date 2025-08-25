import json
import requests

def handler(request):
    from urllib.parse import unquote
    import sys

    try:
        # Get target URL from query parameter
        target_url = request.GET.get("url")
        if not target_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter"}),
                "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            }

        target_url = unquote(target_url)
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(target_url, headers=headers, timeout=10)

        # Return JSON content
        return {
            "statusCode": resp.status_code,
            "body": resp.text,
            "headers": {"Content-Type": resp.headers.get("Content-Type", "application/json"),
                        "Access-Control-Allow-Origin": "*"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        }
