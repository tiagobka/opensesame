
<h1 align='center'>Open Sesame</h1>
<p align=center>
 Real-time facial recognition project
</p>


## Table of Contents

1. [Getting Started](#Getting-Started)
2. [Prerequisites](#Prerequisites)
3. [Installing](#Installing)
4. [Running the tests](#Running-the-tests)

...

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
3. Change configuration and policy files
	```bash 
	nano setup/policy.json
	nano setup/config.json
	```


### Prerequisites

**!The environment installer should automatically install the debian packages and configure the environment!**
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
pip install boto3==1.12.36
pip install picamera
pip install gpiozero
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
