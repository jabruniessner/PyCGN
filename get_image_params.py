import numpy as np
from segmentimage import segment_image


def get_image_params(sample_image, options):
    image = sample_image
    stack = sample_image


    mask = segment_image(stack, options)

    img = stack*mask
    bkg = stack[mask]
    frt = stack[np.logical_not(mask)]
    sig = get_moments(frt)
    noise = get_moments(bkg)

    return img, sig, noise



def get_moments(X, n=3):
    """This functions returns the n first moments of the distribution X"""
    m=np.mean(X)
    X=X-m
    Moments=[np.mean(X**k) for k in range(2, n+1)]
    Moments.insert(0, m)

    return Moments
