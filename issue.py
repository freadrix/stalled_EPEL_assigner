import requests


class Issue(object):
    def __init__(self, issue_title, requester_fas_name, issue_text, issue_url):
        self.issue_text = issue_text
        self.issue_url = issue_url
        self.issue_title = self._skip_unnecessary_symbols(issue_title)
        self._git_url = None
        self.package_name = None
        self._get_package_name()
        self.requester_fas_name = self._analyze_issue_text(requester_fas_name)
        self.is_requester_found = False

    def _analyze_issue_text(self, name_that_opened):
        keywords = ["sig", "fas"]
        self.issue_text = self._skip_unnecessary_symbols(self.issue_text)
        list_of_words_in_text = self.issue_text.split(" ")
        index = list_of_words_in_text.index("requesting")
        if "sig" in self.issue_text:
            sig_name = list_of_words_in_text[index + 1]
            if "@" in sig_name:
                sig_name = sig_name.replace("@", "")
            return sig_name
        else:
            fas_name = list_of_words_in_text[index + 1]
            if len(fas_name) < 5:
                fas_name = list_of_words_in_text[index + 2]
                if len(fas_name) < 5:
                    fas_name = list_of_words_in_text[index + 3]
            return fas_name

    @staticmethod
    def _is_fas_name(name):
        url = "https://fasjson.fedoraproject.org/v1/users/" + name + "/"
        response = requests.get(url=url)
        return response.status_code == 200

    @staticmethod
    def _is_group_name(name):
        url = "https://fasjson.fedoraproject.org/v1/groups/" + name + "/"
        response = requests.get(url=url)
        return response.status_code == 200

    @staticmethod
    def _skip_unnecessary_symbols(text):
        skips = [".", ", ", ":", ";", "'", '"']
        for ch in skips:
            text = text.replace(ch, "")
        return text

    def _get_package_name(self):
        package_prefixes = ("rpms/", "flatpaks/", "modules/", "tests/", "container/")
        issue_title_without_keyword = self.issue_title.split("stalled epel package ")[1]
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
        if self._is_url_valid(git_url):
            self._git_url = git_url

    def _is_url_valid(self, git_url):
        response = requests.get(git_url)
        if response.status_code == 200:
            return True
        else:
            return False
