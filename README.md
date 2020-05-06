

# Open Sesame

**A Facial recognition door lock with AWS and Raspberry Pi**

[![License](http://img.shields.io/:license-MIT-brightgreen.svg)](https://github.com/tiagobka/python-sample-console-app/blob/master/LICENSE) [![Language](https://img.shields.io/badge/Language-Python-blue)](http://doge.mit-license.org) ![Version](https://img.shields.io/badge/Version-v1.0-green)


## Demo
[![Demo](https://i.ytimg.com/vi/UZZMUSrKdxk/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLBorATcMRpZ7uoMH0hCSUuRcfij8A)](https://youtu.be/UZZMUSrKdxk) [![Demo2](https://i.ytimg.com/vi/TvrLyPzLpdo/hqdefault.jpg?sqp=-oaymwEZCPYBEIoBSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLAR3H6daCGq7w5jLo9IX9hVzNkMMA)](https://youtu.be/TvrLyPzLpdo)
 

### Description
Open Sesame is a project that was created for the San José State University Computer Engineering Capstone Project by a group of four undergraduate students. The basic idea of this project was to create a door locking system which used facial recognition in order to determine when to unlock the door. If a person is on the list of acceptable people, the door will unlock. In order to accomplish this we utilized the many services of AWS, such as IAM,  Rekognition, and S3. For the hardware we utilized the Raspberry Pi 3 along with the Pi Camera V2 as the main components. Overall, this project was intended for us to learn and create a product which has real world applications that also encompasses all of our knowledge throughout our time at SJSU. While there are other approaches to this type of project, we decided to focus on learning how to use the services within AWS, as it has become the backbone of almost every field

## Table of Contents

1. [Getting Started](#Getting-Started)
	1.1. [Prerequisites](#Prerequisites)
	1.2. [Installing](#Installing)
	1.3. [Circuit](#Circuit)
	1.4. [AWS setup](#AWS-setup)
2. [Deploying the Facial Recognition](#Deploying-the-Facial-Recognition)
3. [Config Files](#Config-Files)
4. [Authors](#Authors) 
5. [License](#License)
6. [Acknowledgments](#Acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1. Clone the repository
    ```bash
    git clone https://github.com/tiagobka/opensesame
    cd opensesame
    ```
2. Install Environment Requirements
	```bash 
	./environmentinstaller.sh
	```
3. Change [configuration and policy](#Config-Files) files
	```bash 
	nano setup/policy.json
	nano setup/config.json
	```
### Prerequisites

``!The environment installer should automatically install the debian packages and configure the environment!``
- Python 3
- Python packages
	- boto3==1.12.36
	- picamera==1.13
	- gpiozero==1.5.1
- Debian Packages
	- build-essential
	- cmake 
	- pkg-config
	- libjpeg-dev
	- libtiff5-dev
	- libjasper-dev
	- libpng12-dev`
	- libavcodec-dev
	- libavformat-dev
	- libswscale-dev
	- libv4l-dev
	- libxvidcore-devy
	- libx264-dev
	- libgtk2.0-dev
	- libgtk-3-dev
	- libatlas-base-dev
	- gfortran
	- libqtgui4
	- libqt4-test
	- python3-opencv 
		- You may try a different OpenCV installation but this is an easy way to install OpenCV on the RPI3- Raspbian GNU/Linux 10 (buster)


### Installing

If you didn't do it yet, install the package dependencies with the install environment shell script:
```bash 
#inside opensesame directory!
./environmentinstaller.sh
```
You can install the python packages with :
```bash
pip3 install boto3==1.12.36
pip3 install picamera
pip3 install gpiozero
```
### Circuit

***Breadboard view: ***
![Bread Board Circuit](https://bitbucket.org/tiago_benkodosanjos/2020_anjos/raw/33b7feb5f7b909df6eade7e3af389bdb3d2aab82/pub/fig/Senior%20Project_bb.png)

***Circuit Schematic:***

![Schematic](https://bitbucket.org/tiago_benkodosanjos/2020_anjos/raw/33b7feb5f7b909df6eade7e3af389bdb3d2aab82/pub/fig/Senior%20Project_schematic.png)
### AWS setup   
**Step 0: Install and configure AWS Command Line Interface (CLI) on the Raspberry Pi**  
-AWS CLI is a unification tool to control AWS services using the command line.  
-Note: the following command is for pip   
-(install pip from https://pip.pypa.io/en/stable/installing/)  
``` bash
pip install awscli --upgrade --user
```  

Make sure you run the CLI completion command  
```bash 
complete -C aws_completer aws
```  

***Step 1: Configure AWS CLI with appropriate credentials***  

 - Make sure you have a AWS account
	 - [ ] Create a new user
	 - [ ] Give the new user Programmatic Access (for the ability to get the Keys)  
		 - Give the Following Permissions for the User:
		```
		 AWSIoTDataAccess
		 AmazonRekognitionFullAccess
		 AmazonDynamoDBFullAccess  
		 AmazonS3FullAccess 
		 IAMFullAccess
		```
	 - [ ] Figure out you the AWS Region you are in (use the one closest to you) 
	 
	 - [ ] Configuring the AWS CLI
	
		 - Run the following command on the Raspberry Pi 
		```
		aws configure
		AWS Access Key ID [None]: "Put your User's Access Key ID here"
		AWS Secret Access Key [None]: "Put your User's Secret Access Key here"
		Default region name [None]: eu-central-1
		Default output format [None]: json
		```
		
	
	 - [ ] Test the Connection with AWS  
		- Run the following command to see all your registered IoT devices (if you have them)  
		```aws iot list-things```  
	 - [ ] Create a new “Thing” using the AWS CLI   
		 -  Run the following command  
		 ```aws iot create-thing --thing-name "YourThingName"```
		

		
***Step 2: Setting up Amazon S3***  

S3 is used to store the images for the system  
Note: This part can be done either through CLI(below) or the AWS Management Console)

 - Run the following command (for CLI)  
```aws s3 mb s3://guest-images --region eu-west-1```  
Note: Change the name of the bucket and the region for what you are using  

***Step 3: Setting Up AWS Rekognition***  

Rekognition is an extremely powerful tool and through our testing we had certainties around 98% even in low light conditions  

**3.1.** Setting up a collection in AWS Rekognition  
Collections are how AWS Rekognition stores information  
For this project, we used AWS CLI to manage our face collection. If you do not want to use AWS CLI refer to documentation  
Note: The following documentation has instructions to create and manage face collections in many different methods ( Java, AWS CLI, Python, .NET)  
**3.1.1** Run the following command (creates a collection called guest collection)  
```bash
aws rekognition create-collection --collection-id guest_collection--region eu-west-1
```  
Note: Make sure the collection name and region is changed for your specific project   
**3.2.** Adding images “Faces” to the collection created in 3.1.1  
**3.2.1** Run the following command to add images (in CLI)  

```bash
aws rekognition index-faces --image '{"S3Object":{"Bucket":"bucket-name","Name":"file-name"}}'--collection-id " collection-id" --max-faces 9 --quality-filter "AUTO" --detection-attributes "ALL" --external-image-id "example-image.jpg"
```  
Note: Replace the value of collection-id with the name of the collection you want the face to be stored in  
Replace the values of Bucket and Name with the Amazon S3 bucket and image file that you created and uploaded to an S3 Bucket in step 3.1.1  
(for instance “cfCollage.jpg”). The max-faces parameter restricts the number of indexed faces to 9  
Remove or change its value to suit your needs  
Be aware that some systems need escape characters to work:  
e.g : ‘{\"S3Object\":{\"Bucket\":\"bucket-name\", \"Name\":\"file-name\"}}’ 

***Step 4: Creating an IAM Role***  
The previous steps only set up the services though to access the objects an IAM needs to be created  
**4.1.** run the following code in the terminal  
```
	{ 
    	"Version": "2012-10-17", 
   		"Statement": [ 
        	{
             	"Effect": "Allow",
            		"Action": [ 
                	"logs:CreateLogGroup", 
                	"logs:CreateLogStream", 
                	"logs:PutLogEvents" 
                	], 
                	"Resource": "arn:aws:logs:*:*:*"
         	}, 
         	{
             	"Effect": "Allow", 
             	"Action": [ 
                	"s3:GetObject"
                 	], 
                	"Resource": [
                     	"arn:aws:s3:::bucket-name/*" 
                      ]
          	}, 
                    	{ 
            	"Effect": "Allow", 
            	"Action": [ 
                	"rekognition:IndexFaces"
             	],
            	"Resource": "*"
                 	}
             	]
        	}
```  
Note: Make sure the region, account-id, collection names, and buckets are replaced with your items  

***Step 5: Add images to S3 bucket***  
**5.1.** Upload the photo to a S3 Bitbucket using your preferred method (Browser upload,AWS CLI, Boto3 code, etc)   
Note: Boto3 ( is an SDK for AWS allowing to write python code to interact with S3) see 5.0 for installing Boto 3  
optional: 5.0.1 Install Boto3  
**5.0.1** Run the following code  
```sudo pip install boto3```  


## Deploying the Facial Recognition
After setting up the [software](#Getting-Started), [hardware](#Circuit), and [AWS environement](#AWS-setup).

Inside the opensesame directory change to the src folder and run the recognizer script:
```shell
cd src
python3 recognizer.py
```
## Config Files
**config.json** example:
``` json
{
"cascadeFile": "../cascade_models/haarcascade_frontalface_default.xml",
"AccessKeyID": "<AWS_AccessKeyID>",
"SecretKey": "<AWS_SecretAccessKey>",
"region": "<AWS_region>",
"faceCollectionID" : "<AWS_faceCollectionID>",
"pollingTime": 5,
"sensitivity" : 20
}
```
| Field            | Description                                                                                                                                      |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
|cascadeFile   | Indicates which cascade model will be used for facial detection (File path to cascade   model)                                                   |
| AccessKeyID      | AWS access key credential created by AWS IAM (string)                                                                                            |
| SecretKey        | AWS secret key created by AWS IAM (string)                                                                                                       |
| region           | AWS region which has an image bucket and face collection (string)                                                                                |
| faceCollectionID | Name/identification for an AWS face collection (string)                                                                                          |
| pollingTime      | Time the program spends scanning a person’s face (int, seconds)                                                                                  |
| sensitivity      | The minimum threshold to activate AWS facial recognition.nFrames containing a facetotal n Frames in the polling timein   %. (int, percentage)    |

**policy.json** example:
``` json
{
"certaintyThreshold" : 80,
"piggybackAllow": true,
"requestDelay" : 10
}
```
| Field              | Description                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| certaintyThreshold | Minimum facial recognition certainty that unlocks the door (int, percentage)          |
| piggybackAllow     | If one person in the frame is recognized allow others to enter the premises (boolean) |
| requestDelay       | Delay in seconds until a new AWS facial recognition call is allowed (int, seconds)    |


## Authors

* **Tiago Benko Dos Anjos** - *Computer vision & System integration* - [Github Profile](https://github.com/tiagobka) . [Linked In](https://www.linkedin.com/in/tiagobenkodosanjos/)
* **Jacob Balster-Gee** - *Lock Mechanism Design* - [Github Profile](https://github.com/JBalsterG) . [Linked In](https://www.linkedin.com/in/jacob-balster-gee-01a10693/)
* **Shervin Suresh** - *AWS setup* - [Github Profile](https://github.com/shervinsuresh) . [Linked In](https://www.linkedin.com/in/shervin-suresh/)
* **Andre Voloshin** - *Research & Development Facilitator* - [Github Profile](https://github.com/Voloshiraptor) . [Linked In](https://www.linkedin.com/in/andre-voloshin/)


See also the list of [contributors](https://github.com/tiagobka/opensesame/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to Adrian Rosebrock for sharing tips and tricks regarding computer vision
* Special thanks to Dr. Gokay Saldamli for being our advisor for this project
* COVID-19 for not killing everybody in 2020