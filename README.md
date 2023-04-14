# PyCGN
A python implementation of ConfocalGN by Serge Dmitrieff 

Some time ago, I needed a simple confocal image generator for a project that I was working on. I found ConfocalGN by Serge Dimitrieff

https://github.com/SergeDmi/ConfocalGN

https://www.sciencedirect.com/science/article/pii/S2352711017300444

However, later when I was using it, I found that it had a major disadvantage: It is running in Matlab and it was using a lot of ram. Because of the large ram usage I could only run it at the computers of my work, on which Matlab was not running. I first tried Octave, but could not get it to run. I therefore set out to rewrite it in python. Python has the advantage that it is entirely free and open source. Furthermore it can run in google colab, 


This repository contains the result of this work. I myself, found that it works really well!


The functions have mostly the same name as in the original. 

I also attache an example notebook that I wrote in order to test it


Installation:

There is no need for installation, this is just a bunch of python scripts. The only dependencies are numpy, scipy, scikit-image and tifffile



Usage:

The file of main interest is the cgn.py file. The example that I attached takes a custom PSF (measured from our microscope in our lab), a list of flourophore coordinates and a sample image and extract generates a sample image 


However, one could easily use different PSFs and so on. One could also provide a ground truth image or something alike

