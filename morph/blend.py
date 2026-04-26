import cv2
import numpy as np

def cross_dissolve(img1, img2, alpha):
    return (1 - alpha) * img1 + alpha * img2

def laplacian_blend(img1, img2, alpha, levels=4):
    # todo
    pass
