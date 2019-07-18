#Change this information to your preferences########################################################################
CSVFilePath = "~/ChromebookAccessedDates.csv"
SERVICE_ACCOUNT_FILE = '/path/to/service_account_creds.json'
SuperUserEmail = "The email of the user who set up the service account"
###########################################################################################################################

import httplib2
import simplejson as json
from apiclient import discovery
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime
import csv

CSVRows = []
#Set Google API scope
SCOPES = ['https://www.googleapis.com/auth/admin.directory.device.chromeos']

#Path to service account credentials

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
delegated_credentials = credentials.with_subject(SuperUserEmail)

#Authenticate using the service account credentials
service = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)

#Define customer ID
customerID = 'my_customer'

#Create a function to get the results we need
def APICall(nextResultsToken, deviceCount):
	global CSVRows
	pageDeviceCount = 0
	totalDeviceCount = deviceCount
	if nextResultsToken == "":
		results = service.chromeosdevices().list(customerId=customerID,projection='FULL',maxResults=None).execute()
	else:
		results = service.chromeosdevices().list(customerId=customerID,projection='FULL',maxResults=None,pageToken=nextResultsToken).execute()
	jsonOutput = json.dumps(results)
	#print(jsonOutput)
	mydict = json.loads(jsonOutput)
	for item in mydict['chromeosdevices']:
		try:
			DeviceDescription = item['model']
		except:
			DeviceDescription = ""
		try:
			serialNumber = item['serialNumber']
		except:
			serialNumber = ""
		try:
			deviceID = item['deviceId']
		except:
			deviceID = ""
		try:
			orgUnitPath = item['orgUnitPath']
		except:
			orgUnitPath = "/"
		#print(serialNumber)
		try:
			AssetID = item['annotatedAssetId']
		except:
			AssetID = ""
		try:
			ActiveTime = item['activeTimeRanges']
		except:
			ActiveTime = ""
		#ActiveTimeCount = 0
		for ActiveRange in ActiveTime:
			#ActiveTimeCount = ActiveTimeCount + 1
			LastDateAccessed = ActiveRange['date']
		#print LastDateAccessed
		#print ActiveTimeCount
		row = [serialNumber,LastDateAccessed]
		CSVRows.append(row)
		pageDeviceCount = pageDeviceCount + 1
		totalDeviceCount = totalDeviceCount + 1

	print(str(pageDeviceCount) + " devices on this page, " + str(totalDeviceCount) + " devices total.")
	try:
		nextPageToken = results['nextPageToken']
		APICall(nextPageToken, totalDeviceCount)
	except:
		return CSVRows


#Initial call to the API function
APICall(nextResultsToken="", deviceCount = 0)
#print CSVRows

for row in CSVRows:
	print row

with open(CSVFilePath,'w') as writeFile:
	writer = csv.writer(writeFile)
	for row in CSVRows:
		print row
		writer.writerows([row])
writeFile.close()



"""
https://www.googleapis.com/auth/admin.directory.orgunit,https://www.googleapis.com/auth/admin.directory.user,https://www.googleapis.com/auth/admin.directory.device.chromeos



"""
