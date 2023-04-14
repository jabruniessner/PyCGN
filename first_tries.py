import numpy as np
import cgn
import tifffile
import time
from get_image_params import get_image_params
import pymeshlab
import stack_generator
import os 

print(os.path.abspath(__file__))


# def main():
#     sample_image = tifffile.imread("sample_image.tiff")
#     psf=tifffile.imread("MeasuredPSF633.75.tif")
#     ms=pymeshlab.MeshSet()
#     ms.create_sphere()
#     points = ms.current_mesh().vertex_matrix()
#     options=cgn.DEFAULT_OPTIONS["segmentation"]
#     img, sig, noise = get_image_params(sample_image, options)
#     options=cgn.DEFAULT_TRUTH
#     truth = stack_generator.make_ground_truth(points, options)
#     truthimg=truth["img"]
#     seg_options=cgn.DEFAULT_OPTIONS["segmentation"]
#     conf=cgn.DEFAULT_CONF
#     stack, offset = stack_generator.generate_stacks(truth, conf, sig, noise, seg_options)

def main():
    options = cgn.DEFAULT_OPTIONS
    truth = cgn.DEFAULT_TRUTH
    conf = cgn.DEFAULT_CONF

    sample_image = tifffile.imread("/content/gdrive/MyDrive/PyConfocalGN/sample_image.tiff")
    psf=tifffile.imread("/content/gdrive/MyDrive/PyConfocalGN/MeasuredPSF633.75.tif")
    ms=pymeshlab.MeshSet()
    ms.create_sphere(subdiv=8)
    points = ms.current_mesh().vertex_matrix()
    #img, sig, noise = get_image_params(sample_image, options["segmentation"])
    truth["source"]=points
    options["sample_image"]=sample_image
    res, truth_img, sample_prop = cgn.confocal_generator(truth, conf, options)

    image=res["stack"].astype(np.int32)
    tifffile.imwrite("/content/gdrive/MyDrive/PyConfocalGN/new_image.tiff", image)



if __name__ == '__main__':
    starttime=time.time()
    main()
    print(f"The required time was: {(time.time()-starttime):.2f} seconds")
