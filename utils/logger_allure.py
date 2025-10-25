import json
import allure



def attach_request(request_data):
    method = request_data.get("method", "REQUEST")
    url = request_data.get("url", "")
    headers = request_data.get("headers", {})
    cookies = request_data.get("cookies", {})
    body = request_data.get("body", {})

    data = {
        "method": method,
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "body": body
    }
    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name="API Request",
        attachment_type=allure.attachment_type.JSON
    )



def attach_response(response):
    try:
        content = response.json()
    except Exception:
        content = response.text

    data = {
        "status_code": response.status_code,
        "url": response.url,
        "body": content
    }
    allure.attach(
        json.dumps(data, indent=2, ensure_ascii=False),
        name="API Response",
        attachment_type=allure.attachment_type.JSON
    )