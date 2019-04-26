"""
  ___________________________                __ ________        
 /   _____/\_____  \______   \__ __  _______/  |\_____  \______ 
 \_____  \   _(__  <|    |  _/  |  \/  ___/\   __\_(__  <_  __ \
 /        \ /       \    |   \  |  /\___ \  |  | /       \  | \/
/_______  //______  /______  /____//____  > |__|/______  /__|   
        \/        \/       \/           \/             \/       ~ An0n 3xPloiTeR
"""

from config.colors import *

def bucketExists(bucketName):
	bucket 		= f"http://{bucketName}.s3.amazonaws.com"
	request 	= requests.get(bucket)

	if request.status_code 	 == 200:
		return(True)  # Bucket Exists and is:listable
	
	elif request.status_code == 403:
		return(True)  # Bucket Exists and Access's Denied.
	
	else:
		return(False) # Get it ;)

def deleteFile(bucketName, fileName):
	"""
	if `file` exists: then delete
	"""
	path 		= os.getcwd()
	reports_dir	= os.path.join(path, 'reports')
	bucket_pth	= os.path.join(reports_dir, bucketName)
	file 		= os.path.join(bucket_pth, fileName)

	if os.path.isfile(file):
		os.remove(file)

def write(var, color, data):
    if var == None:
        print(color + str(data))
    elif var != None:
        print(w + "[" + g + var + w + "] " + color + str(data))

def _heading(heading, c, var):
    name    = var
    # name    = u'\u2500'
    space   = " " * 7
    var     = str(space + heading + " ..." + space)
    length  = len(var) + 1; print() # \n
    print("{white}" + name * length + name).format(white=w)
    print("{color}" + var).format(color=c)
    print("{white}" + name * length + name).format(white=w); print() # \n

def report(bucketName, fileName, stdout, opt="w"):
	"""
	Useful in dumping output of stdout into /reports/bucketName/specified-file.ext
	Will be integrated soon!
	"""
	path 		= os.getcwd()
	reports_dir	= os.path.join(path, 'reports')
	bucket_pth	= os.path.join(reports_dir, bucketName)
	file 		= os.path.join(bucket_pth, fileName)

	if not(os.path.isdir(reports_dir)):
		os.mkdir(reports_dir)
		if not(os.path.isdir(bucket_pth)):
			os.mkdir(bucket_pth)

	elif os.path.isdir(reports_dir):
	    if not(os.path.isdir(bucket_pth)):
	        os.mkdir(bucket_pth)

	with open(file, opt) as f:
		f.write(stdout)

def heading(heading, bucket, color, afterWebHead):
    space 	= " " * 15
    var 	= str(space + heading + " '" + bucket + "'" + str(afterWebHead) + " ..." + space)
    length 	= len(var) + 1
    
    print()
    print(w + "-" * length + "-")
    print(color + var)
    print(w + "-" * length + "-")
    print()
