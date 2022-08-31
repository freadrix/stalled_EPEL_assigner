from stalled_epel_package_fetcher import StalledEpelPackageFetcher
from issue import Issue
from assigner import Assigner
import requests
from requests_kerberos import HTTPKerberosAuth
import os


def main():
    file_object = open("issues_didnt_process.txt", "w")
    fetcher = StalledEpelPackageFetcher()
    stalled_epel_issues = fetcher.get_issues()
    for issue in stalled_epel_issues:
        if issue.package_name and issue.is_requester_found:
            Assigner(package_name=issue.package_name, fas=issue.requester_name)
        else:
            print(issue.issue_title)
            print(issue.requester_name)
            print(issue.is_requester_found)
            print(issue.package_name)
            print(issue.issue_url)
            print("\n")
            # is_requester_found = issue.is_requester_found
            # is_package_name_found = issue.package_name is None
            # file_object.write(f"Issue with url {issue.issue_url}\n"
            #                   f"had a problem with processing because:\n"
            #                   f"\tis requester found: {is_requester_found}\n"
            #                   f"\tis package name found: {is_package_name_found}\n\n")
    file_object.close()

########    Test processing of single issue     ########################################################################

#     issue_title = "Stalled EPEL package: perl-Number-Bytes-Human"
#     unprocessed_package_name = "perl-Number-Bytes-Human"
#     issue_opener = "robert"
#     issue_text = """
#     Describe the issue
# perl-Number-Bytes-Human is a stalled EPEL package.
# Per the EPEL stalled package policy - https://docs.fedoraproject.org/en-US/epel/epel-policy/#stalled_epel_requests - I have contacted the maintainer, twice, and waited the appropriate amount of time.
# https://bugzilla.redhat.com/show_bug.cgi?id=2115572
# I am a member of the epel-packagers-sig and I am requesting @epel-packagers-sig be given commit permissions so that I, or a member of the SIG, might branch and build this package in epel9. If you change the current RHBZ contact for EPEL, please set it also to @epel-packagers-sig rather than to an individual person.
#
# When do you need this? (YYYY/MM/DD)
# ASAP :)
#
# When is this no longer needed or useful? (YYYY/MM/DD)
# n/a
#
# If we cannot complete your request, what is the impact?
# n/a
#     """
#     issue_url = "https://pagure.io/releng/issue/10992"
#
#     issue = Issue(issue_title=issue_title, unprocessed_package_name=unprocessed_package_name,
#                   issue_opener=issue_opener, issue_text=issue_text, issue_url=issue_url)
#     print(issue.requester_name)
#     print(issue.is_requester_found)
#     print(issue.package_name)
########################################################################################################################


if __name__ == "__main__":
    main()
