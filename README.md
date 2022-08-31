# stalled_EPEL_assigner
## Purpose of app
Application serves for assign requesting person as a contact of EPEL package on Bugzilla.
Reason behind is make issue follow the policy: https://docs.fedoraproject.org/en-US/epel/epel-policy/#stalled_epel_requests.
## Usage
This script is planing to run once at some period of time.
So to do it you need to complete those steps:
1. Get a kerberos authentication `fkinit -u "your FAS"`
2. Write your Pagure API key into config file.
3. Run `runner.py` file
4. Issues that couldn't be processed you can find in `issues_didnt_process.txt` file. You need to handle it by yourself.

