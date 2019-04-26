# S3Rec0n
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![python](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/)
[![GitHub version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6.0.1&v=6.0.1&x2=0)](http://badge.fury.io/gh/boennemann%2Fbadges)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

**A colorful cross-platform python utility to test misconfigurations of buckets both through authenticated and unauthenticated checks!**

<img src="https://i.imgur.com/7r96xmg.png" />

### S3Rec0n's Output
<img src="https://i.imgur.com/ooPyx6z.gif">

### Requirements

- Python (3.7.*)
- Python `pip3`
- Python module `boto3`
- Python module `botocore`
- Python module `jmespath`
- Python module `pygments`
- Python module `requests`

### Install python && modules
	
	sudo apt install python3 python3-pip python3-venv
	mkdir ~/.venvs/S3Rec0n/ && python3 -m venv ~/.venvs/S3Rec0n/ && source ~/.venvs/S3Rec0n/bin/activate
	pip install -r requirements.txt

### Tested on

- Pop! OS 18.04
- Kali linux (2019.1)
- Ubuntu 18.04 LTS
- Windows 8/8.1/10
- Subsystem Linux
 
### Download/Clone S3Rec0n

You can download the latest version of S3Rec0n by cloning the GitHub repository. As a best practice, please use python's virtual environment (venv) while running the script to avoid any modules/packages installation errors. 

	git clone https://github.com/Ebryx/S3Rec0n

### Usage

***Initializing Script***

	python s3rec0n.py

***Listing Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --list-bucket --bucket=myTestBucket

***Listing Bucket with S3 API Authorization (using access keys)***

    python s3rec0n.py --authorized --list-bucket --bucket=myTestBucket

***Listing Bucket without specifying any flag both auth/unauth S3 API Call (by default it gets set to unauthorized)***

    python s3rec0n.py --list-bucket --bucket=myTestBucket

***Fetching ACL of the Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --get-acl --bucket=myTestBucket

***Putting/Over-writing the ACL of the Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --put-acl --bucket=myTestBucket

***Fetching readable objects of the Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --readable-objs --bucket=myTestBucket

***Trying and uploading a test object on the Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --upload-objs --bucket=myTestBucket

***Fetching ACLs of all the objects of the Bucket without S3 API Authorization (anonymously)***

    python s3rec0n.py --unauthorized --fetch-obj-acl --bucket=myTestBucket

### Advanced Usage

<pre><code>
Author: Syed Umar Arfeen

Usage: python s3rec0n.py
A colorful cross-platform python utility to test misconfigurations of buckets both through authenticated and unauthenticated checks!

Features/Functions:

 1). Authenticated Checks (through access keys)
 2). Unauthenticated Checks (anonymously)
 3). Buckets Location (AWS Region)
 4). Static Website Hosting Check
 5). Bucket Listing
 6). Fetching ACL (Access Control List) of the Bucket
 7). Over-writing ACL of the bucket (be careful!)
 8). Finding readable objects in the bucket
 9). Uploading test key/object for misconfiguration test
 10). Fetch ACLs of all the Objects
  
  Example:
	python s3rec0n.py
</code></pre>

### Screenshots

<img src="https://i.imgur.com/Vl823MN.gif">
<img src="https://i.imgur.com/nemCSxO.gif">
<img src="https://i.imgur.com/X7GCe8y.gif">
<img src="https://i.imgur.com/Vl823MN.gif">


### Note 
<pre><code>Do not change the position of any module as given under the Usage, this may cause an failure in the working of the script...
P.S ~ Dont Change The Colors. They're Butiphul like this.
	~ An0n 3xPloiTeR
</code></pre>
