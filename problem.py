import os,sys,math
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import aircv as ac
import cv2
import handler
import util

class ProblemHandler(handler.Handler):
    def __init__(self, imgSrc, phone, store):
        super(ProblemHandler, "pics/problemSign.jpg", phone)
        self.y0 = 0
        self.peaks = []
        self.store = store
    
    def check(self, imgSrc) -> bool:
        self.imgSrc = ac.imread(imgSrc)
        res = util.match(self.imgSrc, self.imgSign)
        if res != None :
            self.y0 = res['rectangle'][3][1] + 10
            return True
        return False
    
    def handle(self):
        self.getInfo()


    def getInfo(self):
        self.imgSrcEn = cv2.convertScaleAbs(self.imgSrc, alpha=1.5, beta=0)
        w, h, _ = self.imgSrc.shape
        hist = [0] * h
        for i in range(y0, h):
            for j in range(0, w):
                p = pix[j, i]
                if p[0] < 50 and p[1] < 50 and p[2] < 50:
                    hist[i] += 1
        self.peaks = util.findPeaks(hist, 50, 10)
        if len(self.peaks) <= 0:
            return
        
        

        

    def learn(self):
        pass
    
    def answer(self):
        pass


def findCeil():
    imgSrc = ac.imread("e.jpg")
    imgObj = ac.imread("b.jpg")
    res = ac.find_template(imgSrc, imgObj, 0.5)
    print(res)
    return res['rectangle'][3][1]

y0 = int(findCeil()) + 10

im = Image.open('e.jpg')
enhanceContrast = ImageEnhance.Contrast(im)
im = enhanceContrast.enhance(1.5)

pix = im.load()
w, h = im.size
hist = [0] * h
for i in range(y0, h):
    for j in range(0, w):
        p = pix[j, i]
        if p[0] < 50 and p[1] < 50 and p[2] < 50:
            hist[i] += 1

peaks = peak.findPeaks(hist, 50, 10)
print(peaks)

for ps in peaks:
    rect = [0, ps[0], w-1, ps[1]]
    imCrop = im.crop(rect)
    #imCrop.show()


plt.plot(hist)
plt.show()