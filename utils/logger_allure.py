import json
import allure



def attach_request(method, url, headers=None, body=None, cookies=None):
    data = {
        "method": method,
        "url": url,
        "headers": headers or {},
        "cookies": cookies or {},
        "body": body or {}
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