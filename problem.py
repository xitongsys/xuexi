import os,sys,math
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import peak
import aircv as ac

class Problem:
    def __init__(self, imgSrc):
        self.imgSrc = imgSrc
        self.imgSign = "pics/problemSign.jpg"
        self.y0 = 0
    
    def check(self) -> bool:
        imgSrc = ac.imread(self.imgSrc)
        imgObj = ac.imread(self.imgSign)
        res = ac.find_template(imgSrc, imgObj, 0.5)
        if res != None :
            self.y0 = res['rectangle'][3][1] + 10
            return True
        return False
    
    def handle(self):
        pass

    def getInfo(self):
        self.im = Image.open(self.imgSrc)
        enhanceContrast = ImageEnhance.Contrast(self.im)
        self.im = enhanceContrast.enhance(1.5)
        pix = self.im.load()
        w, h = self.im.size
        hist = [0] * h
        for i in range(y0, h):
            for j in range(0, w):
                p = pix[j, i]
                if p[0] < 50 and p[1] < 50 and p[2] < 50:
                    hist[i] += 1

        self.peaks = peak.findPeaks(hist, 50, 10)

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