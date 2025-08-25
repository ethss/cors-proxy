import json
import requests
from urllib.parse import unquote

def handler(request):
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return {
            "statusCode": 204,
            "body": "",
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
        }

    try:
        target_url = request.GET.get("url")
        if not target_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
            }

        target_url = unquote(target_url)
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(target_url, headers=headers, timeout=15)

        # Try to parse JSON safely
        try:
            data = resp.json()
            body = json.dumps(data)
            content_type = "application/json"
        except:
            body = resp.text
            content_type = resp.headers.get("Content-Type", "text/plain")

        return {
            "statusCode": resp.status_code,
            "body": body,
            "headers": {
                "Content-Type": content_type,
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
            },
        }

    except requests.exceptions.RequestException as e:
        # Network/timeout errors
        return {
            "statusCode": 502,
            "body": json.dumps({"error": f"Request failed: {str(e)}"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
