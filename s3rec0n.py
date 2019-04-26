from jmespath import search as queryJson
from re import findall as parseRegex
from pygments import highlight, lexers, formatters
from requests import get
from json import loads, dumps
from time import sleep
from io import StringIO
from config import *
from config.config import _usage
import botocore
import boto3
import argparse

class S3:
	def __init__(self, bucket):
		self.bucket 	= bucket

	def parseJson(self, query, jsonObj):
		return(queryJson(query, jsonObj))

	def prettifyJSON(self, jsonObject):
		return(highlight(jsonObject, lexers.JsonLexer(), formatters.TerminalFormatter()))

	def authorizedClientCall(self):
		"""
		Makes Authorized Client call to S3 (picks up access keys from ~/.aws/)
		"""
		client 		= boto3.client("s3")
		return(client)

	def unAuthorizedClientCall(self):
		"""
		Makes Unauthorized Client call to S3 (i.e. without access keys)
		"""
		client 		= boto3.client("s3", config=botocore.config.Config(signature_version=botocore.UNSIGNED))
		return(client)

	def getBucketLocation(self, bucketName):
		"""
		Returns bucket['LocationConstraint']
		Doesn't work with unsigned requests
		So, had to come up with a solution of mine B)
		"""
		_bucket 		= f"http://{bucketName}.s3.eu-west-1.amazonaws.com"
		request 		= get(_bucket)
		sourceCode 		= request.content.decode('UTF-8')
		regex 			= r'\<Endpoint\>(.*?)\<\/Endpoint\>'
		location 		= parseRegex(regex, sourceCode)
		result 			= ""
		
		if "s3.amazonaws.com" in str(location): 
			result 		= f"http://{bucketName}.{location[0]}"
		
		elif len(location) == 0: 
			result 		= _bucket
		
		else: 
			result 		= f"http://{location[0]}"

		write(var="$", color=w, data=result)
		return(result)

	def fetchBucketACL(self, clientCall, bucketName):
		"""
		As the name of the function depicts: It fetches / downloads `ACLs` of the bucket...
		"""

		try:
		    response 	= clientCall.get_bucket_acl(Bucket=bucketName)
		    print(self.prettifyJSON(dumps( self.parseJson("Grants", response), indent=4 )))

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "GetBucketAcl" in e.args[0]:
				write(var=f"{r}!", color=w, data=f"It seems we can't fetch the {r}ACL{w} of this bucket :(")

	def overWriteBucketACL(self, clientCall, bucketName):
		"""
		Overwrites the current ACL of the bucket even if we aren't able to fetch the ACL of the bucket
		Sounds crazy! huh!?
		"""
		bucketACL = {
	        'Owner': {
	            'ID': '694f79fd87bab72d3576779c0a2308cc3b2006dfe0e76105562755d701e8c2e1'
	        },
	        'Grants': [
	            {
	                'Grantee': {
	                    'Type': 'Group',
	                    'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'
	                },
	                'Permission': 'FULL_CONTROL'
	            },
	        ],
	    }

		try:
			ACL 	= loads(dumps((lambda c, b: c.get_bucket_acl(Bucket=b))(clientCall, bucketName)))['Grants'][0]['Permission']
			
			if ACL == 'FULL_CONTROL':
				write(var=f"{c}#", color=w, data=f"It seems we already have {g}FULL_CONTROL{w} over the bucket! :P\n")
				return

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "GetBucketAcl" in e.args[0]: pass

		try: 
			putACL 	= (lambda a, b, c: a.put_bucket_acl(Bucket=b, AccessControlPolicy=c))(clientCall, bucketName, bucketACL)
			write(var=f"{c}#", color=w, data=f"It seems we were able to {g}overwrite{w} the ACL of the bucket, lets confirm {y}:)\n")

			try:
				bucketACL 	= loads(dumps((lambda c, b: c.get_bucket_acl(Bucket=b))(clientCall, bucketName)))['Grants'][0]
				print(self.prettifyJSON(dumps(bucketACL, indent=4)))
				permissions	= bucketACL['Permission']
				URI 		= bucketACL['Grantee']['URI']

				if (URI == "http://acs.amazonaws.com/groups/global/AllUsers" and permissions == "FULL_CONTROL"):
					write(var=f"{c}$", color=w, data=f"{r}Hell yeah{w}, {g}we did it{w}!")

				else:
					write(var=f"{r}!", color=w, data=f"It seems we {r}weren't successful{w} in over-writing the {c}ACL{w} of the bucket! {r}:(")

			except botocore.exceptions.ClientError as e:
				if "AccessDenied" and "GetBucketAcl" in e.args[0]: write(var=f"{r}!", color=w, data=f"It seems we {r}weren't successful{w} in over-writing the {c}ACL{w} of the bucket! {r}:(")

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "PutBucketAcl" in e.args[0]: write(var=f"{r}!", color=w, data=f"It seems we can't {r}overwrite{w} the {r}ACL{w} of this bucket :(")

	def listBucket(self, clientCall):
		"""
		Lists the objects in the buckets both through authorized and `--no-sign-request`
		Returns False if unauthorized listing of objects is set to false 
		"""
		try:
			response 	= clientCall.list_objects(Bucket=self.bucket)
			response 	= self.parseJson("Contents[].Key", response)

			for objects in response:
				write(var=f"{g}#", color=w, data=f"{objects}")
				sleep(0.01)

			return(response)

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "ListObjects" in e.args[0]:
				return(None)

	def readableObjects(self, clientCall, bucket, objectsList):
		"""
		Checks in the objects list provided, if the objects are readable
		TL;DR if readable: return contentOfObject else: None
		"""
		readableObjs 		= []
		for objects in objectsList:

			try:
				response 	= clientCall.get_object( Bucket=bucket, Key=objects )
				response 	= response['ResponseMetadata']['HTTPStatusCode']
				write(var=f"{c}#", color=w, data="{:<65} -~> {}{}".format(objects, g, response))
				readableObjs.append(objects)
				sleep(0.01)

			except botocore.exceptions.ClientError as e:
				if "AccessDenied" and "GetObject" in e.args[0]:
					write(var=f"{r}!", color=w, data="{:<65} -~> {}{}".format(objects, r, 403))

		return(readableObjs)

	def uploadObjectOnBucket(self, clientCall, bucketName):
		dataToWrite		= b"Pentesting in Progress"
		keyName 		= 'pentest0bject.txt'

		try:
			response 		= clientCall.put_object(Body=dataToWrite, Bucket=bucketName, Key=keyName, ACL="public-read-write")
			write(var=f"{c}@", color=w, data=f"Awesome! We just {g}uploaded{w} our object at {g}{bucketName}/{keyName}")

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "PutObject" in e.args[0]:
				write(var=f"{r}!", color=w, data=f"It seems we {r}failed{w} to upload {r}0bject{w} on the {c}bucket{w} {r}:(")

	def fetchObjectsACL(self, clientCall, bucketName, objectsList):
		for objects in objectsList:
			try:

				if objects[::-1][0] != "/":
					response 	= clientCall.get_object_acl(Bucket=bucketName, Key=objects)
					response 	= loads(dumps(response))['Grants']
					write(var=f"{g}$", color=w, data=f"ACL of \"{g}{objects}{w}\"")
					print( self.prettifyJSON(dumps(response, indent=4)) )
					sleep(0.01)

			except botocore.exceptions.ClientError as e:
				if "AccessDenied" and "GetObjectAcl" in e.args[0]:
					write(var=f"{r}!", color=w, data=f"ACL of {r}\"{objects}\"{w} isn't accessible!")

	def checkBucketStaticHosting(self, clientCall, bucketName):
		try:
			response = clientCall.get_bucket_website(Bucket=bucketName)
			print(response)

		except botocore.exceptions.ClientError as e:
			if "AccessDenied" and "GetBucketWebsite" in e.args[0]:
				write(var=f"{r}!", color=w, data=f"The bucket doesn't have {r}static hosting{w} enabled!")

def main():
	print(banner)
	parser 		= argparse.ArgumentParser(description='', usage=f'{_usage}{b}')
	parser._optionals.title = "Basic Help"

	basicFuncs 	= parser.add_argument_group(f'{g}Actions')
	basicFuncs.add_argument('--bucket', 				action="store", 		dest="bucket", 	 		default=False, help='Bucket to test the script against!')	
	basicFuncs.add_argument("-au", 	"--authorized", 	action="store_true", 	dest="authorized", 		default=False, help="Perform the checks using Access Keys")
	basicFuncs.add_argument("-ua", 	"--unauthorized", 	action="store_true", 	dest="unauthorized",	default=False, help="Perform the checks anonymously!")
	basicFuncs.add_argument('-a', '--all', 				action="store_true", 	dest="all", 	 		default=False, help='To run all the functions against the bucket!')

	functions 	= parser.add_argument_group(f'{y}Functions')
	functions.add_argument("-l", 	"--location", 		action="store_true", default=False,	dest="location", 		help="Find the Bucket's Location")
	functions.add_argument("-s", 	"--static-hosting", action="store_true", default=False,	dest="staticHosting", 	help="Finds if the bucket has Static Hosting enabled")
	functions.add_argument("-ba", 	"--get-acl", 		action="store_true", default=False, dest="getBucketACL", 	help="Fetches the ACL of the Bucket")
	functions.add_argument("-pa", 	"--put-acl", 		action="store_true", default=False,	dest="putBucketACL", 	help="Puts the ACL with FULL_CONTROL on the bucket")
	functions.add_argument("-lb", 	"--list-bucket", 	action="store_true", default=False,	dest="listBucket", 		help="List the S3 Bucket Objects/Keys")
	functions.add_argument("-r", 	"--readable-objs", 	action="store_true", default=False,	dest="read0bjs", 		help="Finds the readable 0bjects/Keys")
	functions.add_argument("-up", 	"--upload-objs", 	action="store_true", default=False,	dest="upload0bjs", 		help="Uploads a test 0bject on the S3 Bucket")
	functions.add_argument("-oa", 	"--fetch-obj-acl", 	action="store_true", default=False,	dest="read0bjsACL", 	help="Finds the ACL of Individual 0bjects/Keys")

	args = parser.parse_args()
	if args.bucket:
		bucket 			= args.bucket
		S30bj 			= S3(bucket)

		#############################################################################

		if args.unauthorized:
			clientCall 		= S30bj.unAuthorizedClientCall()

		elif args.authorized:
			clientCall 		= S30bj.authorizedClientCall()

		else:
			write(var=f"{r}!", color=w, data=f"No flags were specified for API Calls, moving with unauthorized API Calls")
			clientCall 		= S30bj.unAuthorizedClientCall()

		#############################################################################

		if args.location:
			heading(heading="Finding Location/Region of", 		bucket=bucket, color=c, afterWebHead="")
			S30bj.getBucketLocation(bucket)

		elif args.staticHosting:
			heading(heading="Finding Static Web Hosting 0n", 	bucket=bucket, color=y, afterWebHead="")
			S30bj.checkBucketStaticHosting(clientCall, bucket)

		elif args.getBucketACL:
			heading(heading="Fetching the ACL of", 				bucket=bucket, color=g, afterWebHead="")
			S30bj.fetchBucketACL(clientCall, bucket)

		elif args.putBucketACL:
			heading(heading="Trying to 0verwrite the ACL 0f", 	bucket=bucket, color=b, afterWebHead="")
			S30bj.overWriteBucketACL(clientCall, bucket)

		elif args.listBucket:
			heading(heading="Listing Objects of", 				bucket=bucket, color=y, afterWebHead="")
			S30bj.listBucket(clientCall)

		elif args.read0bjs:
			heading(heading="Listing Objects of", 				bucket=bucket, color=r, afterWebHead="")
			S30bjs 	= S30bj.listBucket(clientCall)

			if not(S30bjs == None):
				heading(heading="Reading/Fetching 0bjects 0f", 	bucket=bucket, color=m, afterWebHead="")
				S30bj.readableObjects(clientCall, bucket, S30bjs)

			elif S30bjs == None:
				write(var=f"{r}!", color=w, data=f"It seems we {r}don't{w} have {r}listing / read objects{w} permissions on the bucket {r}:(")

			else:
				write(var=f"{r}!", color=w, data=f"No {r}keys/objects{w} found in the S3 bucket: {r}{bucket}")

		elif args.upload0bjs:
			heading(heading="Trying to Upload 0bject on", 		bucket=bucket, color=g, afterWebHead="")
			S30bj.uploadObjectOnBucket(clientCall, bucket)

		elif args.read0bjsACL:
			heading(heading="Listing Objects of", 				bucket=bucket, color=r, afterWebHead="")
			S30bjs 	= S30bj.listBucket(clientCall)

			if not(S30bjs == None):
				heading(heading="Fetching ACLs 0f", 			bucket=bucket, color=g, afterWebHead=" 0bjects")
				S30bj.fetchObjectsACL(clientCall, bucket, S30bjs)

			elif S30bjs == None:
				write(var=f"{r}!", color=w, data=f"It seems we {r}don't{w} have {r}listing / read objects{w} permissions on the bucket {r}:(")

			else:
				write(var=f"{r}!", color=w, data=f"No {r}keys/objects{w} found in the S3 bucket: {r}{bucket}")

		elif args.all:
			heading(heading="Finding Location/Region of", 		bucket=bucket, color=c, afterWebHead="")
			S30bj.getBucketLocation(bucket)
			sleep(0.1)

			heading(heading="Finding Static Web Hosting 0n", 	bucket=bucket, color=y, afterWebHead="")
			S30bj.checkBucketStaticHosting(clientCall, bucket)
			sleep(0.1)

			heading(heading="Fetching the ACL of", 				bucket=bucket, color=g, afterWebHead="")
			S30bj.fetchBucketACL(clientCall, bucket)
			sleep(0.1)

			heading(heading="Trying to 0verwrite the ACL 0f", 	bucket=bucket, color=b, afterWebHead="")
			S30bj.overWriteBucketACL(clientCall, bucket)
			sleep(0.1)

			heading(heading="Listing Objects of", 				bucket=bucket, color=y, afterWebHead="")
			S30bjs 	= S30bj.listBucket(clientCall)
			sleep(0.1)

			if not(S30bjs == None):
				heading(heading="Reading/Fetching 0bjects 0f", 	bucket=bucket, color=m, afterWebHead="")
				S30bj.readableObjects(clientCall, bucket, S30bjs)
				sleep(0.1)

				heading(heading="Fetching ACLs 0f", 			bucket=bucket, color=g, afterWebHead=" 0bjects")
				S30bj.fetchObjectsACL(clientCall, bucket, S30bjs)
				sleep(0.1)

			elif S30bjs == None:
				write(var=f"{r}!", color=w, data=f"It seems we {r}don't{w} have {r}listing / read objects{w} permissions on the bucket {r}:(")

			else:
				write(var=f"{r}!", color=w, data=f"No {r}keys/objects{w} found in the S3 bucket: {r}{bucket}")

		else:
			write(var=f"{r}!", color=w, data=f"Please specify an argument to execute! :(")

		#############################################################################

	else:
		parser.print_help()
		exit(footer)

	print(footer)

if __name__ == '__main__':
	main()
