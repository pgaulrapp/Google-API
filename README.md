# Google-API
Python scripts for use with Google's APIs

1. Turn on API access in your Google Admin Console

2. Turn on the API SDK.

3. Create an API service account, with the relevant scopes for directory access. You need the following scope for this script:
https://www.googleapis.com/auth/admin.directory.device.chromeos

4. Make sure the Google API client for Python is installed on your computer:

pip install --upgrade google-api-python-client --user
pip install google-auth-oauthlib --user

5. Change the lines at the top of the script to match the information for your Google domain.

Run the script and see what happens. If everything is properly set up, you should have a CSV file with serial numbers and the dates of the last access for each serial.
