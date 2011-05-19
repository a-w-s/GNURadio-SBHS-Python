Introduction
============

GNURadio-SBHS-Python contains the setup files written in python for installing Data Acquisition Block for Single Board Heater System (SBHS) in GNURadio.  There are two blocks both written in python.

	1. SBHS Source - Acts as a source for the device.
	2. Plot Sink   - Plots the temperature reading against time.

For detailed information visit: http://spoken-tutorial.org/wiki/index.php/GNURadio_Documentation#Open_Source_Data_Acquisition_System

Pre-Requisites
==============

This package requires that gnuradio-core, python, matplotlib, hal, wxpython, numpy is already installed.  It also depends on some GNU Radio pre-requisites, such as Boost, Python2.6-dev and Cppunit.

For a complete list of Pre-requisites visit: http://gnuradio.org/redmine/wiki/gnuradio/BuildGuide

Building & Compiling
====================

To build and compile do the following inside the directory:

	$ sudo autoconf
	$ sudo ./bootstrap
	$ sudo ./configure
	$ cd swig
	$ sudo make generate-makefile-swig
	$ cd ..
	$ sudo make
	$ sudo make install
	$ sudo ldconfig

