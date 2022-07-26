import struct

import requests
from requests_kerberos import HTTPKerberosAuth


class Issue(object):
    def __init__(self, issue_title, issue_opener, issue_text, issue_url):
        self.issue_text = self._skip_unnecessary_symbols(self._make_text_lower(issue_text))
        self.is_requester_found = False
        self.requester_name = self._get_requester_name()
        self.issue_url = issue_url
        self.issue_title = issue_title
        self.package_name = self._get_package_name()
        self._git_url = None

    @staticmethod
    def _make_text_lower(text):
        return text.lower()

    @staticmethod
    def _skip_unnecessary_symbols(text):
        skips = [".", ", ", ":", ";", "'", '"', "@", "`"]
        for ch in skips:
            text = text.replace(ch, "")
        return text

    @staticmethod
    def _strip_each_element(list_of_words):
        new_list_of_words = list(map(str.strip, list_of_words))
        return new_list_of_words

    def _get_requester_name(self):
        list_of_words_in_text = self.issue_text.split(" ")
        list_of_words = self._strip_each_element(list_of_words_in_text)
        index = list_of_words.index("requesting")
        fas_name_index = self._get_fas_name_index(index, list_of_words)
        if fas_name_index != 0:
            return list_of_words[fas_name_index]
        else:
            return "FAS is not found"

    def _get_fas_name_index(self, index, list_of_words):
        for index_offset in range(1, 4):
            new_index = index + index_offset
            fas_name = list_of_words[new_index]
            if self._is_group_name(fas_name) or self._is_fas_name(fas_name) and len(fas_name) > 4:
                self.is_requester_found = True
                return new_index
        return 0

    @staticmethod
    def _is_fas_name(name):
        url = "https://fasjson.fedoraproject.org/v1/users/" + name + "/"
        response = requests.get(url=url, auth=HTTPKerberosAuth())
        return response.status_code == 200

    @staticmethod
    def _is_group_name(name):
        url = "https://fasjson.fedoraproject.org/v1/groups/" + name + "/"
        response = requests.get(url=url, auth=HTTPKerberosAuth())
        return response.status_code == 200

    def _get_package_name(self):
        package_prefixes = ("rpms/", "flatpaks/", "modules/", "tests/", "container/")
        if "stalled epel package" in self.issue_title.lower():
            unprocessed_package_name = self.issue_title[21:].strip()
        else:
            unprocessed_package_name = self.issue_title
        if unprocessed_package_name.startswith(package_prefixes):
            self._get_git_url(unprocessed_package_name)
            if self._is_git_url_valid():
                return unprocessed_package_name
        else:
            for prefix in package_prefixes:
                package_name = prefix + unprocessed_package_name
                self._get_git_url(package_name)
                if self._is_git_url_valid():
                    return package_name
        return None

    def _try_different_prefixes(self, package_name, prefixes):
        for prefix in prefixes:
            package_name_with_prefix = prefix + package_name
            self._get_git_url(package_name_with_prefix)
            if self._git_url:
                self.package_name = package_name_with_prefix
                return True
        return False

    def _get_git_url(self, package_name):
        git_url = "https://src.fedoraproject.org/" + package_name + ".git"
        self._git_url = git_url

    def _is_git_url_valid(self):
        response = requests.get(self._git_url)
        if response.status_code == 200:
            return True
        else:
            return False
