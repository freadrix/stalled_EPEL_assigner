from stalled_epel_package_fetcher import StalledEpelPackageFetcher


def main():
    fetcher = StalledEpelPackageFetcher()
    stalled_epel_issues = fetcher.get_issues()
    print(stalled_epel_issues)


if __name__ == "__main__":
    main()
