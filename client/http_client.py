import http.client
import json

headers = {
    "Accept": "application/json",
    "User-Agent": "PyQt6-Client/1.0"
}


class HttpClient:
    def __init__(self, url):
        self.url = url

    def get(self, uri: str) -> dict[str, object]:
        conn = http.client.HTTPConnection(self.url)
        conn.request("GET", uri, headers=headers)

        response = conn.getresponse()
        conn.close()

        return json.loads(response.read().decode("utf-8"))
