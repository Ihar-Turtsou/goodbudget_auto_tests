import requests

class GBApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def login(self, username, password):
        self.session.get(f"{self.base_url}/login", timeout=15)
        resp = self.session.post(
            f"{self.base_url}/login_check",
            data={"_username": username, "_password": password},
            allow_redirects=False,
            timeout=15,
        )
        assert resp.status_code in (302, 303), f"Login failed: {resp.status_code}"
        cookie = self.session.cookies.get("GBSESS")
        assert cookie, "GBSESS cookie not set"
        return cookie

    def close(self):
        self.session.close()
