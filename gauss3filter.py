import numpy as np


def gauss3filter(image, sigma, pixelspacing=(1,1,1)):

    size=image.shape
    sigma1, sigma2, sigma3 = (*sigma, *sigma, *sigma) if len(sigma)==1 else sigma

    sigma1=sigma1^2
    sigma2=sigma2^2
    sigma3=sigma3^2

    u,v,w =ifftshiftedcoormatrix3(size)

    u=u/size[0]/pixelspacing[0]
    v=v/size[1]/pixelspacing[1]
    w=w/size[2]/pixelspacing[2]

    fil=GaussianKernel(u, v, w, sigma1, sigma2, sigma3)



    fil=fil+GaussianKernel(u+1/pixelspacing[0], v, w, sigma1, sigma2, sigma3)
    fil=fil+GaussianKernel(u-1/pixelspacing[0], v, w, sigma1, sigma2, sigma3)
    fil=fil+GaussianKernel(u, v+1/pixelspacing[1], w, sigma1, sigma2, sigma3)
    fil=fil+GaussianKernel(u, v-1/pixelspacing[1], w, sigma1, sigma2, sigma3)
    fil=fil+GaussianKernel(u, v, w+1/pixelspacing[2], sigma1, sigma2, sigma3)
    fil=fil+GaussianKernel(u, v, w-1/pixelspacing[2], sigma1, sigma2, sigma3)


    fil=fil/np.max(fil)
    del u, v, w

    result = np.real(np.fft.ifftn(np.fft.fftn(image)*fil))



    return result


def GaussianKernel(u, v, w, sigma1, sigma2, sigma3):
    return np.exp(-2*np.pi**2*(u**2*sigma1+v**2*sigma2+w**2*sigma3))


def ifftshiftedcoormatrix3(dimension):
    """This function gives the ifftshifted coordinates in the frequency domain"""
    varargout=[]
    for idx, d in enumerate(dimension):
        p = int(d/2)
        a = [n-p for n in range(p, d)]+[n-p for n in range(p)]
        dim_ = list(dimension)
        del dim_[idx]
        A = np.empty((*dim_, len(a)))
        A[:,:] = a
        B=np.moveaxis(A, -1, idx)
        varargout.append(B)


    return varargout



def main():
    a=np.array([1,2,3,4])
    sigma=(1,)
    gauss3filter(a, sigma)
    sigma=(1,2,3)
    gauss3filter(a, sigma)

if __name__ == '__main__':
    main()
