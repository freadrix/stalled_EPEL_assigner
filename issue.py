import requests

class Issue(object):
    def __init__(self, issue_title, requester_fas_name):
        self._issue_title = self._skip_unnecessary_symbols(issue_title)
        self._git_url = None
        self.package_name = None
        self._get_package_name()
        self.requester_fas_name = requester_fas_name

    def _skip_unnecessary_symbols(self, issue_title):
        skips = [".", ", ", ":", ";", "'", '"']
        for ch in skips:
            issue_title = issue_title.replace(ch, "")
        return issue_title

    def _get_package_name(self):
        package_prefixes = ("rpms/", "flatpaks/", "modules/", "tests/", "container/")
        issue_title_without_keyword = self._issue_title.split("stalled epel package ")[1]
        list_of_words_in_title = issue_title_without_keyword.split(" ")
        for word in list_of_words_in_title:
            if word.startswith(package_prefixes):
                self._get_git_url(word)
                if self._git_url:
                    self.package_name = word
                    return
            else:
                if self._try_different_prefixes(word, package_prefixes):
                    return

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
        if self._is_git_url_exist(git_url):
            self._git_url = git_url

    def _is_git_url_exist(self, git_url):
        response = requests.get(git_url)
        if response.status_code == 200:
            return True
        else:
            return False


