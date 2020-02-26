import os,sys,math
import matplotlib.pyplot as plt
import aircv as ac
import cv2
import handler
import util

class ProblemHandler(handler.Handler):
    def __init__(self, imgSrc, phone, store):
        super().__init__("problem", "pics/problemSign.jpg", phone)
        self.y0 = 0
        self.peaks = []
        self.store = store
        self.problem = None
        self.answers = []
        self.w, self.h = 0, 0
    
    def check(self, imgSrc) -> bool:
        self.imgSrc = ac.imread(imgSrc)
        res = util.match(self.imgSrc, self.imgSign)
        if res != None :
            self.y0 = res['rectangle'][3][1] + 10
            return True
        return False
    
    def handle(self):
        self.getInfo()
        self.answer()


    def getInfo(self):
        self.imgSrcEn = cv2.convertScaleAbs(self.imgSrc, alpha=1.5, beta=0)
        # cv2.imshow('image', self.imgSrcEn)
        # cv2.waitKey(0)

        self.h, self.w, _ = self.imgSrc.shape
        hist = [0] * self.h
        for i in range(self.y0, self.h):
            for j in range(0, self.w):
                p = self.imgSrcEn[i, j]
                if p[0] < 100 and p[1] < 100 and p[2] < 100:
                    hist[i] += 1
        # plt.plot(hist)
        # plt.show()

        self.peaks = util.findPeaks(hist, 50, 10)
        if len(self.peaks) <= 0:
            return
        
        bi, ei = self.peaks[0]
        self.problem = self.imgSrc[bi:ei, 0:self.w]
        self.answers = []
        for p in self.peaks[1:]:
            bi, ei = p
            self.answers.append(self.imgSrc[bi:ei, 0:self.w])


    def learn(self):
        pass
    
    def answer(self):
        if self.problem is None:
            return
            
        answer = self.store.find(self.problem)
        if answer is None:
            self.tapAnswer(0)
            self.captureAnswer()
        else:
            idx = util.findImg(self.answers, answer)
            self.tapAnswer(idx)
        

    def tapAnswer(self, idx):
        if idx+1 >= len(self.peaks):
            return
        bi, ei = self.peaks[idx + 1]
        self.phone.tap(int(self.w/2), int((bi+ei)/2))

    def captureAnswer(self):
        capturePath = "inputs/a0.png"
        self.phone.screencast(capturePath)
        imgAnswer = cv2.imread(capturePath)
        answerColor = [61, 192, 118]
        
        mindis, minidx = -1, 1
        for pi in range(1, len(self.peaks)):
            b, e = self.peaks[pi]
            s = 0
            for i in range(b, e):
                for j in range(0, self.w):
                    cp = imgAnswer[i, j]
                    dis = util.dis(answerColor, cp)
                    s += dis

            if mindis < 0 or mindis > s:
                mindis, minidx = s, pi
      
        self.store.add(self.problem, self.answers[minidx - 1])



