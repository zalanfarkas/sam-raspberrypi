# README

# SAM-RASPBERRYPI application 

Part of the SAM (Student Attendance Monitoring) project of Team Foxtrot 2018 at University of Aberdeen

Copyright (c) 2018 Team Foxtrot

Licensed under MIT License

## Getting started

* If you don’t have python preinstalled, install it by typing following command to command prompt:
	```
	sudo apt-get install python2.7-dev
	```
* Install pip (python package manager)
	- Go to pip.pypa.io install[2] page and follow install instructions
* Enable SPI device
	- Go to /etc/modprobe.d/raspi-blackist.conf and remove # from blacklist i2c-bcm2708 line
* Download SPI-Py package by opening command prompt and entering:
	```
	git clone https://github.com/lthiery/SPI-Py
	```
* Install SPI-Py package by typing following command to command prompt:
	```
	sudo apt-get-install python-dev
	```
*  Install GPIO python package by entering following commands to command prompt:
	```
	wget https://pypi.python.org/packages/source/R/RPi.GPIO-0.5.4.tar.gz
	```
	```
	tar zxf RPi.GPIO-0.5.4.tar.gz
	```
	```
	cd RPi.GPIO-0.5.4
	```
	```
	sudo python setup.py install
	```
* Install Request library
* Add dependencies for fingerprint sensor
	```
	wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -
	```
	```
	wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.list.d/
	```
 
* Install python fingerprint library
	```
	apt-get update
	```
	```
	apt-get install python-fingerprint --yes
	```

 [2] https://pip.pypa.io/en/stable/installing/
