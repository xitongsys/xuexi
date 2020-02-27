import os,sys,math
import cv2
import aircv as ac
import matplotlib.pyplot as plt
from skimage import measure


def findPeaks(data, maxInterval, threshold = 25):
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

def match(imgSrc, imgSign, threshold=0.95) -> bool:
    res = ac.find_template(imgSrc, imgSign, threshold)
    return res

def similarity(img1, img2):
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape
    if abs(h1-h2)/max(h1,h2) > 0.1:
        return -1

    h, w = min(h1,h2), min(w1, w2)    
    img1 = cv2.resize(img1, (w, h))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img2, (w,h))
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return measure.compare_ssim(img1, img2)

def findImg(imgs, tar, threshold = 0.9):
    maxSim, maxidx = -1, 0
    for i in range(0, len(imgs)):
        s = similarity(imgs[i], tar)
        if s > maxSim:
            maxSim, maxidx = s, i
    
    print("=====", maxSim)
    if maxSim > threshold:
        return maxidx
    
    return -1

def resizeToGrayImg(img, scale):
    h, w, _ = img.shape
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def resizeImg(img, scale):
    h, w, _ = img.shape
    img = cv2.resize(img, (int(w*scale), int(h*scale)))
    return img
    

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