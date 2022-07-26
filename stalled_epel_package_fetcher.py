import requests
from issue import Issue


class StalledEpelPackageFetcher(object):
    def __init__(self):
        self._params = {
            "status": "Closed",
            "per_page": 20
        }
        self._keyword = "stalled epel package:"
        self._api_endpoint = "https://pagure.io/api/0/releng/issues"

    def get_issues(self):
        list_of_issues = []
        number_of_pages = self._get_number_of_pages()
        for page in range(5):  # for _ in range(number_of_pages)
            self._params["page"] = page + 1
            response = requests.get(url=self._api_endpoint, params=self._params)
            issues = response.json()["issues"]
            # print(issues)
            for issue in issues:
                issue_title = issue["title"]
                if self._is_contain_keyword(issue_title):
                    issue_opener = issue["user"]["name"]
                    issue_url = issue["full_url"]
                    issue_text = issue["content"].lower()
                    issue = Issue(issue_title, issue_opener, issue_text, issue_url)
                    list_of_issues.append(issue)
                self._params["page"] += 1
        return list_of_issues

    def _get_number_of_pages(self):
        response = requests.get(url=self._api_endpoint, params=self._params)
        number_of_pages = response.json()["pagination"]["pages"]
        return number_of_pages

    def _is_contain_keyword(self, issue_title):
        return self._keyword in issue_title.lower()
