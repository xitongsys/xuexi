import os,sys,math
import cv2
import aircv as ac
import matplotlib.pyplot as plt
from skimage import measure


def findPeaks(data, maxInterval, threshold = 50):
    res = []
    ln = len(data)
    i = 0
    while i < ln:
        b = i
        while b < ln and data[b] < threshold:
            b += 1

        i, j = b, b
        while i < ln:
            if data[i] >= threshold:
                i, j = i + 1, i
            elif i - j < maxInterval:
                i += 1
            else:
                break
        if b < ln and j - b > 5:
            res.append([b, j])
    return res

def match(imgSrc, imgSign, threshold=0.8) -> bool:
    res = ac.find_template(imgSrc, imgSign, threshold)
    return res

def similarity(img1, img2):
    h, w, _ = img2.shape
    img1 = cv2.resize(img1, (h, w))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img2, (h,w))
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return measure.compare_ssim(img1, img2)

def findImg(imgs, tar, threshold = 0.9):
    for i in range(0, len(imgs)):
        if similarity(imgs[i], tar) > threshold:
            return i
    return -1

def dis(a, b):
    ln = len(a)
    s, ds = 0, 0
    for i in range(0, ln):
        ds += (a[i] - b[i])**2
        s += a[i]**2
    return ds/s



# def match(imgSrc, imgObj):
#     img1 = cv2.imread('inputs/a.jpg')
#     img2 = cv2.imread('pics/entrySign.jpg')
#     img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#     #sift
#     keypoints_1, descriptors_1 = pysift.computeKeypointsAndDescriptors(img1)
#     keypoints_2, descriptors_2 = pysift.computeKeypointsAndDescriptors(img2)

#     print(keypoints_1, keypoints_2)

# if __name__ == '__main__':
#     match(0,0)