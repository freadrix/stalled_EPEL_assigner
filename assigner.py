import requests


class Assigner(object):
    """ Assigner to bz. """

    def __init__(self, package_name, fas):
        self.endpoint = "https://src.fedoraproject.org/_dg/bzoverrides/" + package_name
        self.assign_fas(fas)

    def assign_fas(self, fas):
        data = {"Maintainer name": fas,
                "EPEL Maintainer name": fas
                }
        response = requests.post(url=self.endpoint, json=data)
        print(response.status_code)
