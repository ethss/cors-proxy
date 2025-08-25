from urllib.parse import unquote
import requests
import json

def handler(request):
    # Handle preflight
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
        target_url = request.args.get("url")  # instead of request.GET.get
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

        method = request.method.upper()
        data = request.data if method in ["POST", "PUT", "PATCH"] else None

        resp = requests.request(method, target_url, headers=headers, data=data, timeout=10)

        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}
        response_headers["Access-Control-Allow-Origin"] = "*"
        response_headers["Access-Control-Allow-Methods"] = "*"
        response_headers["Access-Control-Allow-Headers"] = "*"

        return {
            "statusCode": resp.status_code,
            "body": resp.text,
            "headers": response_headers,
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
