from stalled_epel_package_fetcher import StalledEpelPackageFetcher
from issue import Issue
import requests
from requests_kerberos import HTTPKerberosAuth
import os


def main():
    fetcher = StalledEpelPackageFetcher()
    stalled_epel_issues = fetcher.get_issues()
    for issue in stalled_epel_issues:
        print(issue.requester_name)
        print(issue.is_requester_found)
        print(issue.package_name)
        print(issue.issue_url)
        # print("\n")

#     issue_title = "Stalled EPEL package: perl-Text-CSV"
#     issue_opener = "robert"
#     issue_text = """
#     libappindicator is a stalled EPEL package.
#
# Per the EPEL stalled package policy - https://docs.fedoraproject.org/en-US/epel/epel-policy/#stalled_epel_requests - the maintainer has been contacted twice, and I have waited the appropriate amount of time.
#
# https://bugzilla.redhat.com/show_bug.cgi?id=2062984
#
# Therefore, as a member of the EPEL Packager SIG, I am requesting @epel-packagers-sig to be added as co-maintainer to the package so that I or another member of the SIG may branch and build this package for EPEL.
#
# Please also add myself (@ngompa), @salimma, and @dcavalca as co-maintainers.
#     """
#     issue_url = "https://pagure.io/releng/issue/10861"
#     #
#     issue = Issue(issue_title=issue_title, issue_opener=issue_opener, issue_text=issue_text, issue_url=issue_url)
#     print(issue.requester_name)
#     print(issue.is_requester_found)
    # print(issue.package_name)
    # print(issue_text)
    # test_str = "Stalled EPEL Package: DSADASDas-ss"
    # test_str_after_lower = None
    # if "packages" in test_str.lower():
    #     pass
    # else:
    #     test_str_after_lower = test_str[21:]
    # print(test_str_after_lower)
    # print(issue.issue_url)
    # print(issue.requester_name)
    # print(issue.is_requester_found)
    # print("\n")

if __name__ == "__main__":
    main()
