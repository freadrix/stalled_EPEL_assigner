from stalled_epel_package_fetcher import StalledEpelPackageFetcher
import requests
import os


def main():
    # os.system("fkinit -u amedvede")
    response = requests.get(url="https://fasjson.fedoraproject.org/v1/groups/epel-packagers-sig/")
    print(response.status_code, response.json())
    # fetcher = StalledEpelPackageFetcher()
    # stalled_epel_issues = fetcher.get_issues()
    # for issue in stalled_epel_issues:
    #     print(issue.package_name)
    #     print(issue.issue_url)
    #     print(issue.requester_fas_name)
    #     # print(issue.is_requester_found)
    #     print("\n")


if __name__ == "__main__":
    main()
