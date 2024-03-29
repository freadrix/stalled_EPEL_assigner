import requests
from requests_kerberos import HTTPKerberosAuth


def skip_unnecessary_symbols(text):
    skips = [".", ", ", ":", ";", "'", '"', "@", "`"]
    for ch in skips:
        text = text.replace(ch, "")
    return text


def strip_each_element(list_of_words):
    new_list_of_words = list(map(str.strip, list_of_words))
    return new_list_of_words


class Issue(object):
    """ Contain info about single issue """
    def __init__(self, issue_title, unprocessed_package_name, issue_opener, issue_text, issue_url):
        self.issue_text = skip_unnecessary_symbols(issue_text.lower())
        self.is_requester_found = False
        self.requester_name = self._get_requester_name(issue_opener)
        self.issue_url = issue_url
        self.issue_title = issue_title
        self.package_name = self._get_package_name(unprocessed_package_name)
        self._git_url = None

    def _get_requester_name(self, issue_opener):
        list_of_words_in_text = self.issue_text.split(" ")
        list_of_words = strip_each_element(list_of_words_in_text)
        try:
            index = list_of_words.index("requesting")
        except ValueError:
            return None
        fas_name_index = self._get_fas_name_index(index, list_of_words)
        if fas_name_index is not None:
            return list_of_words[fas_name_index]
        else:
            return None

    def _get_fas_name_index(self, index, list_of_words):
        for index_offset in range(1, 5):
            new_index = index + index_offset
            fas_name = list_of_words[new_index]
            if self._is_group_name(fas_name) or self._is_fas_name(fas_name) and len(fas_name) > 4:
                self.is_requester_found = True
                return new_index
        return None

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

    def _get_package_name(self, unprocessed_package_name):
        package_namespaces = ("rpms/", "flatpaks/", "modules/", "tests/", "container/")
        if unprocessed_package_name.startswith(package_namespaces):
            self._get_git_url(unprocessed_package_name)
            if self._is_git_url_valid():
                return unprocessed_package_name
        elif unprocessed_package_name == "Unhandled_issue":
            return None
        else:
            for namespace in package_namespaces:
                package_name = namespace + unprocessed_package_name
                self._get_git_url(package_name)
                if self._is_git_url_valid():
                    return package_name
        return None

    def _get_git_url(self, package_name):
        git_url = "https://src.fedoraproject.org/" + package_name + ".git"
        self._git_url = git_url

    def _is_git_url_valid(self):
        response = requests.get(self._git_url)
        if response.status_code == 200:
            return True
        else:
            return False
