# Python Image Labelling GUI

![intro](Screenshots/Intro_Label.png)

Table of contents
-----------------

* [Introduction](#introduction)
* [Requirements and Installation](#requirements-and-installation)
* [Intro Screen](#into-screen)
* [Grid Cell Labelling](#grid-cell-labelling)
* [Bounding Box Labelling](#bounding-box-labelling)
* [Polygon Labelling](#polygon-labelling)
* [FAQ](#faq)

Introduction
------------

A GUI made in Python that can label all images in a folder with different coloured labels. The program supports bounding box labelling, polygon labelling and individual grid-cell labelling.

**Python Image Labeller**

* Uses callback events from Matplotlib to label images
* Labels can be saved in .json format or in csv format. In the case of generic region labelling, labels can be saved as new images.
* Supports multiple labels to be added to images with custom colours
* Allows user to label all images stored in one particular folder
* Options to adjust colour and size of measurement grid#

Requirements and Installation
-----------------------------

The following packages are required and were tested with the following versions:

* Matplotlib version 3.2.1
* keyboard 0.13.4

Clone the repository into a folder and run `Image Labeller.py` in a Python kernel. I.e. `python ImageLabeller.py` in the command line.

Intro Screen
------------

The intro screen can be used to load an image for labelling. Click on the `Browse` button in the bottom right corner.

![bottom](Screenshots/Bottom_Bar.png)

Select an image the file explorer. You need to select an image in order to start labelling so that previous labels in the folder can be loaded.
 
![imageSelect](Screenshots/Image_Select.png)

After you have selected the image that you want to label. Select a button on the top bar to select a method for labelling.

![top](Screenshots/Top_Bar.png)
