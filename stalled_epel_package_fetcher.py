import requests


class StalledEpelPackageFetcher(object):
    def __init__(self):
        self._params = {
            "status": "Closed",
            "per_page": 20
        }
        self._keyword = "stalled epel package"
        self._api_endpoint = "https://pagure.io/api/0/releng/issues"

    def get_issues(self):
        response = requests.get(url=self._api_endpoint, params=self._params)
        return response.json()
