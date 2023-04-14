from random import random
import numpy as np
import tifffile
import scipy
from skimage.filters import threshold_otsu
from gauss3filter import gauss3filter
from get_image_params import get_image_params
from stack_generator import stack_generator
import os



DEFAULT_OPTIONS = {
"segmentation":{
                "filt":[1, 1, 0],
                  "ix":[],
                },
"sampling":{
            "filt": [1, 1, 0],
            "ix": [n for n in range(9, 17)]
            },
"format": "single",

"verbose": 1,

"sample_image": tifffile.imread("/content/gdrive/MyDrive/PyConfocalGN/sample_image.tiff")
}


DEFAULT_TRUTH = {
"image_size": np.array([55, 512, 512]),
"pix_size": np.array([490.9, 31.68, 31.68]),
"offset":np.array([0, 0, 0]),
"overscale": 1.5,
"pts_scale":512*31.68,
"format": "single",
"flourophore": "poisson",
"background": np.array([0, 0, 0]),
"verbose": 1,
"signal":np.array([100])
}

DEFAULT_CONF = {"psf":tifffile.imread("/content/gdrive/MyDrive/PyConfocalGN/MeasuredPSF31.68.tif"),
"pix": np.array([490.9, 31.68 , 31.68])}




def confocal_generator(truth = DEFAULT_TRUTH, conf=DEFAULT_CONF, options=DEFAULT_OPTIONS):
    sample_options = options["sampling"]
    sample = truth["source"]
    img, sig, noise = get_image_params(options["sample_image"], sample_options)
    res, truth = stack_generator(truth, conf, sig, noise, options)
    sample_prop = {"sig":sig, "noise": noise}
    return res, truth , sample_prop
