import numpy as np
from math import ceil
from random import random
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter
from get_image_params import get_image_params
import tifffile


def stack_generator(truth, conf, sig, noise, options):
    truth_options=truth
    truth = make_ground_truth(truth["source"], truth_options)
    seg_options = options["segmentation"]

    #generating stacks
    
    stack, offset = generate_stacks(truth, conf, sig, noise, seg_options)
    img , SIG, NOISE = get_image_params(stack, seg_options)

    res={"stack": stack, "offset":offset, "sig": SIG, "noise": NOISE, "img":img }

    print("Target:")
    print(f"        signal       {sig}")
    print(f"        noise        {noise}")
    print(f"        signal/noise {sig[0]/noise[0]}")
    print("Achieved:")
    print(f"        signal       {SIG}")
    print(f"        noise        {NOISE}")
    print(f"        signal/noise {SIG[0]/NOISE[0]}")

    print(f"The last results shape is {stack.shape}")
    print(f"The last results max is {np.max(stack)}")

    return res, truth


def make_ground_truth(source, options):
    img, points, pix = make_img_from_points(source, options)
    truth = {"source":source, "img": img,"points": points,"pix": pix}
    return truth


def make_img_from_points(input, options):

    fluo = options["signal"]
    bkgd = options["background"]
    mode = options["flourophore"]
    sizes = options["image_size"]
    offset = options["offset"]
    pixsizes = options["pix_size"]
    overscale = options["overscale"]
    pts_scale = options["pts_scale"]

    points = input

    s = points.shape

    if pts_scale is not None:
        points=points*pts_scale

    points=points/pixsizes

    print(pixsizes)




    points = points + np.ones(3)*offset
    #Keeping only points inside
    for i in range(3):
        points = points[points[:, i] < sizes[i]]
        points = points[points[:, i] > 0]


    #creating an image from these points
    img = generate_image(sizes, points, fluo, bkgd, mode)


    return img, points, pixsizes


def generate_image(Sizes, RR, fluo, bkgd, mode='gamma'):
    if len(bkgd)<3:
        bkgd[2]=0.

    sN = Sizes.shape

    if sN[0]==1:
        Sizes=np.array([Sizes[0], Sizes[0], Sizes[0]])

    img = np.zeros(Sizes)
    s=RR.shape
    NS=s[0]
    
    sig = pixel_distribution(fluo, NS, mode)
    
    if np.min(sig)<0:
      sig=sig-np.min(sig)

    #Summing the flourescence to each voxel
    #We count the flourophores per high-res voxel and add te flourescnece to the image
    A, _, toA =np.unique(np.round(RR).astype(int), axis=0, return_index=True, return_inverse=True)
    nA = A.shape[0]
    sigA = np.zeros(nA)


    #Heuristic to save time in flourescence assignment
    if nA<4*NS:
        for i in range(nA):
            sigA[i]=sigA[toA[i]]+np.sum(sig[toA==i])
    else:
        for i in range(NS):
            sigA[toA[i]] = sigA[toA[i]]+sig[i]


    for idx, a in enumerate(A):
        img[a[0]-1, a[1]-1, a[2]-1] = sigA[idx]


    ## Adding the background
    # Added to every points

    if bkgd[2]==0:
        #if no skew, gaussian noise
        print("We are using the normal distribution")
        bg = np.random.normal(loc=bkgd[0], scale=bkgd[1], size=Sizes)
    else:
        
        px_off, k, theta = gamma_params(bkgd)
        if k < 0 or theta < 0:
            print("We are using the normal distribution")
            #not enough skew back to gaussian noise
            bg = np.random.normal(loc=bkgd[0], scale=bkgd[1], size=Sizes)
        else:
            print("We are using the gamma distribution")
            bg = px_off + np.random.gamma(k, theta, img.shape)

    img=img+bg


    return img


def generate_stacks(truth, conf, sig, noise, options):
    img=truth["img"]
    psf=conf["psf"]


    if len(psf)<4:
        psf=psf/truth["pix"]

    pix=conf["pix"]/truth["pix"]

    img=convolve_with_psf(img, psf)


    stack, offset, nn = stack_from_img(img, pix)

   

    px_noise = pixel_distribution(noise, nn)



    img2, Ssignal, Snoise = get_image_params(stack, options)

    #Desired signal to noise
    S=Ssignal[0]
    B=Snoise[0]
    SNR = sig[0]/noise[0]

    b = np.absolute((S-SNR*B)/(SNR-1))
    a=np.absolute(1/(B+b))
    stack=a*(stack+b)

    #We multiply the stack by the noise (why?)

    if np.min(px_noise)<0:
      px_noise=px_noise-np.min(px_noise)


    

    stack=stack*px_noise


    return stack, offset






def convolve_with_psf(image, psf):
    if len(psf.shape)==1:
        new = gaussian_filter(image, sigma=psf, truncate=2.0)
    else:
        new=fftconvolve(image, psf, mode="same")
    return new



def pixel_distribution(list_moments, NP, mode="gamma"):
    if mode == "gamma":
        if  list_moments[2]==0:
            px_distr=list_moments[0]+np.sqrt(list_moments[2])*box_muller(NP)
        else:
            print("Using gamma distribution in pixel distribution")
            px_off, k, theta=gamma_params(list_moments)
            if k<0 or theta<0:
                #not enough skew, back to gaussian distribution
                px_distr=list_moments[0]+np.sqrt(list_moments[1])*box_muller(NP)
            else:
                px_distr=px_off+np.random.gamma(shape=k, scale=theta, size=NP)

    elif mode == "poisson":
        print("Using poisson in pixel distribution")
        px_distr = np.random.poisson(lam=list_moments[0],size=NP)

    else:
        px_distr = np.ones(NP)*list_moments[0]
    return px_distr




def gamma_params(M):
    theta = 0.5 *M[2]/M[1]
    k = M[2]/(theta**2)
    offset = M[0]-k*theta
    return offset, k, theta




def box_muller(n):
    a=np.random.random(n)
    b=np.random.random(n)
    v1=np.sqrt(-2*np.log(a))*np.sin(2*np.pi*b)
    v2=np.sqrt(-2*np.log(a))*np.cos(2*np.pi*b)
    return v1, v2




def stack_from_img(img, pix):
    s = np.array(img.shape)
    nn = (s/pix).astype(int)

    di = pix[0]/2
    dj = pix[1]/2
    dk = pix[2]/2

    offset=[-di, -dj, -dk]

    range1=[n+int(di) for n in range(0, nn[0]*int(pix[0]))]
    range2=[n+int(dj) for n in range(0, nn[1]*int(pix[1]))]
    range3=[n+int(dk) for n in range(0, nn[2]*int(pix[2]))]


    stack =  img[range1]
    stack =  img[:, range2]
    satck =  img[:, :, range3]

    return stack, offset, nn
