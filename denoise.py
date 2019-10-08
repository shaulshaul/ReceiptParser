# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2gray

def main():
    img2 = cv2.imread('noisy1.png')
    img = rgb2gray(img2) * 255
    # plot the noisy image
    plt.subplot(141)
    plt.imshow(img, cmap='gray')
    plt.title('noisy')

    plt.subplot(142)
    plt.imshow(denoise_gray(img, weight=1), cmap='gray')
    plt.title('denoising with small weight')

    plt.subplot(143)
    plt.imshow(denoise_gray(img, weight=10), cmap='gray')
    plt.title('denoising with medium weight')

    plt.subplot(144)
    plt.imshow(denoise_gray(img, weight=100), cmap='gray')
    plt.title('denoising with strong weight')
    plt.show()

    # remove noise using median filter
    # plt.subplot(121)
    # plt.imshow(img2)
    # plt.subplot(122)
    # plt.imshow(median_filtering(img2))
    # #plt.imshow(sharpening(median_filtering(img2)))
    # plt.show()

    print(1)

def denoise_gray(img, weight=0.1, eps=1e-3, num_iter_max=200):
    """Perform total-variation denoising on a grayscale image.

    Parameters
    ----------
    img : array
        2-D input data to be de-noised.
    weight : float, optional
        Denoising weight. The greater `weight`, the more
        de-noising (at the expense of fidelity to `img`).
    eps : float, optional
        Relative difference of the value of the cost
        function that determines the stop criterion.
        The algorithm stops when:
            (E_(n-1) - E_n) < eps * E_0
    num_iter_max : int, optional
        Maximal number of iterations used for the
        optimization.

    Returns
    -------
    out : array
        De-noised array of floats.

    Notes
    -----
    Rudin, Osher and Fatemi algorithm.
    """
    u = np.zeros_like(img)
    px = np.zeros_like(img)
    py = np.zeros_like(img)

    nm = np.prod(img.shape[:2])
    tau = 0.125

    i = 0
    while i < num_iter_max:
        u_old = u

        # x and y components of u's gradient
        ux = np.roll(u, -1, axis=1) - u
        uy = np.roll(u, -1, axis=0) - u

        # update the dual variable
        px_new = px + (tau / weight) * ux
        py_new = py + (tau / weight) * uy

        norm_new = np.maximum(1, np.sqrt(px_new **2 + py_new ** 2))
        px = px_new / norm_new
        py = py_new / norm_new

        # calculate divergence
        rx = np.roll(px, 1, axis=1)
        ry = np.roll(py, 1, axis=0)
        div_p = (px - rx) + (py - ry)

        # update image
        u = img + weight * div_p

        # calculate error
        error = np.linalg.norm(u - u_old) / np.sqrt(nm)

        if i == 0:
            err_init = error
            err_prev = error
        else:
            # break if error small enough
            if np.abs(err_prev - error) < eps * err_init:
                break
            else:
                e_prev = error

        # don't forget to update iterator
        i += 1

    return u

def median_filtering(img):
    median = cv2.medianBlur(img,5)
    return median

def sharpening(img):
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    # applying the sharpening kernel to the input image & displaying it.
    sharpened = cv2.filter2D(img, -1, kernel_sharpening)
    return sharpened



if __name__ == '__main__':
    main()