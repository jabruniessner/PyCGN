import gauss3filter
import tifffile
import time


image=tifffile.imread("sample_image.tiff")
starttime=time.time()
b=gauss3filter.gauss3filter(image, (3,))
print(f"The required time was {(time.time()-starttime):.2f}")
