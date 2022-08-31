import requests
from config import API_KEY


class Assigner(object):
    """ Assigner to bz. """

    def __init__(self, package_name, fas):
        self.endpoint = "https://src.fedoraproject.org/_dg/bzoverrides/" + package_name
        self.headers = {"Authorization": f"token {API_KEY}"}
        self.assign_fas(fas)

    def assign_fas(self, fas):
        data = {"EPEL Maintainer name": fas}
        previous_fas = self._get_previous_epel_fas()
        if fas == previous_fas:
            print("200 nothing need to change")
        else:
            response = requests.post(url=self.endpoint, headers=self.headers, json=data)
            print(response.status_code)

    def _get_previous_epel_fas(self):
        response = requests.get(url=self.endpoint)
        return response.json()["epel_assignee"]
