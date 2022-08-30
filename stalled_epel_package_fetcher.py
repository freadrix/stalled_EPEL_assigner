import requests
import re
from issue import Issue
from issue import skip_unnecessary_symbols, strip_each_element


class StalledEpelPackageFetcher(object):
    """ Fetcher releng issues. """
    def __init__(self):
        self._list_of_issue_objs = []
        self._issue = None
        self._params = {
            "status": "Closed",
            "per_page": 20
        }
        self._list_of_words_in_keyword = ["stalled", "epel", "package"]
        self._keyword_for_single_issue = "stalled epel package:"
        self._keyword_for_multiple_issues = "stalled epel packages:"
        self._api_endpoint = "https://pagure.io/api/0/releng/issues"

    def get_issues(self):
        """ Observe all pages and test all issues. """
        number_of_pages = self._get_number_of_pages()
        for page in range(5):  # for _ in range(number_of_pages)
            self._params["page"] = page + 1
            response = requests.get(url=self._api_endpoint, params=self._params)
            issues = response.json()["issues"]
            for issue in issues:
                self._issue = issue
                self._select_type_of_issue()
                self._params["page"] += 1
        return self._list_of_issue_objs

    def _select_type_of_issue(self):
        """ Select type of issue. """
        issue_title = self._issue["title"]
        if self._is_contain_words_from_keyword(issue_title):
            if self._is_contain_keyword_for_single_issue(issue_title):
                self._process_issue()
            elif self._is_contain_keyword_for_multiple_issues(issue_title):
                self._process_issues()
            else:
                self._unhandled_issue()

    def _process_issue(self):
        """ Process issue that contain single EPEL package. """
        issue_title = self._issue["title"]
        issue_opener = self._issue["user"]["name"]
        issue_url = self._issue["full_url"]
        issue_text = self._issue["content"].lower()
        unprocessed_package_name = issue_title[len(self._keyword_for_single_issue):].strip()
        issue_obj = Issue(issue_title, unprocessed_package_name, issue_opener, issue_text, issue_url)
        self._list_of_issue_objs.append(issue_obj)

    def _process_issues(self):
        """ Process issue that contain multiple EPEL packages. """
        issue_title = self._issue["title"]
        issue_opener = self._issue["user"]["name"]
        issue_url = self._issue["full_url"]
        issue_text = self._issue["content"]
        unprocessed_package_names = issue_title[len(self._keyword_for_multiple_issues):].strip()
        unprocessed_package_names = self._skip_unnecessary_words_between_package_names(unprocessed_package_names)
        list_of_package_names = unprocessed_package_names.split(" ")
        list_of_package_names = strip_each_element(list_of_package_names)
        if list_of_package_names[0].isnumeric():
            amount_of_packages = int(list_of_package_names[0])
            package_prefix = list_of_package_names[1]
            if package_prefix.endswith("s"):
                package_prefix = package_prefix[:len(package_prefix) - 1]
            list_of_package_names = self._get_package_names(issue_text, amount_of_packages, package_prefix)
        for package_name in list_of_package_names:
            issue_obj = Issue(issue_title, package_name, issue_opener, issue_text, issue_url)
            self._list_of_issue_objs.append(issue_obj)

    def _unhandled_issue(self):
        """ Process issue that can't be handled. """
        issue_title = self._issue["title"]
        issue_opener = "Unhandled_issue"
        issue_url = self._issue["full_url"]
        issue_text = "Unhandled_issue"
        unprocessed_package_name = "Unhandled_issue"
        issue_obj = Issue(issue_title, unprocessed_package_name, issue_opener, issue_text, issue_url)
        self._list_of_issue_objs.append(issue_obj)

    @staticmethod
    def _get_package_names(text, amount_of_packages, package_prefix):
        list_of_package_names = []
        list_of_words_in_text = strip_each_element(re.split(r'" "|\r|\n', skip_unnecessary_symbols(text)))
        list_of_words_in_text = [el for el in list_of_words_in_text if el]
        for i in range(len(list_of_words_in_text)):
            if list_of_words_in_text[i].startswith(package_prefix):
                for i_offset in range(amount_of_packages):
                    list_of_package_names.append(list_of_words_in_text[i + i_offset])
                return list_of_package_names
        return None

    @staticmethod
    def _skip_unnecessary_words_between_package_names(package_names):
        unnecessary_words = ["and"]
        for word in unnecessary_words:
            package_names = package_names.replace(word, "")
        return package_names

    def _get_number_of_pages(self):
        response = requests.get(url=self._api_endpoint, params=self._params)
        number_of_pages = response.json()["pagination"]["pages"]
        return number_of_pages

    def _is_contain_words_from_keyword(self, issue_title):
        return all(word in issue_title.lower() for word in self._list_of_words_in_keyword)

    def _is_contain_keyword_for_single_issue(self, issue_title):
        return self._keyword_for_single_issue in issue_title.lower()

    def _is_contain_keyword_for_multiple_issues(self, issue_title):
        return self._keyword_for_multiple_issues in issue_title.lower()
