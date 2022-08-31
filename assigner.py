import requests


class Assigner(object):
    """ Assigner to bz. """

    def __init__(self, package_name, fas):
        self.endpoint = "https://src.fedoraproject.org/_dg/bzoverrides/" + package_name
        self.assign_fas(fas)

    def assign_fas(self, fas):
        data = {"EPEL Maintainer name": fas}
        previous_fas = self._get_previous_epel_fas()
        if fas == previous_fas:
            print("200 nothing need to change")
        else:
            response = requests.post(url=self.endpoint, json=data)
            print(response.status_code)

    def _get_previous_epel_fas(self):
        response = requests.get(url=self.endpoint)
        return response.json()["epel_assignee"]
