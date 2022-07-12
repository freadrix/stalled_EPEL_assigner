from stalled_epel_package_fetcher import StalledEpelPackageFetcher


def main():
    fetcher = StalledEpelPackageFetcher()
    stalled_epel_issues = fetcher.get_issues()
    for issue in stalled_epel_issues:
        print(issue.package_name)


if __name__ == "__main__":
    main()
