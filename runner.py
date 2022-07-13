from stalled_epel_package_fetcher import StalledEpelPackageFetcher


def main():
    fetcher = StalledEpelPackageFetcher()
    stalled_epel_issues = fetcher.get_issues()
    for issue in stalled_epel_issues:
        print(issue.package_name)
        print(issue.is_requester_who_opened_issue)
        print(issue.issue_url)


if __name__ == "__main__":
    main()
