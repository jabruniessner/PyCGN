import numpy as np
import time
from gauss3filter import gauss3filter
from skimage.filters import threshold_otsu



def segment_image(image, options = None):

    assert options != None

    filt=options["filt"]
    ix=options["ix"]
    img = gauss3filter(image, filt)
    img1, bg_mask, t = threshold(img)
    sg_mask = np.logical_not(bg_mask)

    return bg_mask



def threshold(img, t=None):
    if t==None:
        t=threshold_otsu(img)
    no = (img < t)
    img1 = no*img
    return img1, no, t
