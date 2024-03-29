import os,sys,math,time
import matplotlib.pyplot as plt
import aircv as ac
import cv2
import handler, util, paras

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
        res = util.match(self.imgSrc, self.imgSign, 0.9)
        if res != None :
            self.y0 = int(res['rectangle'][3][1] + 80*paras.SCALE)
            return True
        return False
    
    def handle(self):
        print("Handle problem")
        cv2.imwrite("problems_backup/{:06d}.png".format(paras.INDEX), self.imgSrc)
        paras.INDEX += 1
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

        self.peaks = util.findPeaks(hist, 25, 2)
        # print(self.peaks)

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
            print("answer not found")
            self.tapAnswer(0)
            self.captureAnswer()
        else:
            res = util.match(self.imgSrc, answer)
            if res is None:
                print("answer not match")
                self.tapAnswer(0)
                self.captureAnswer()
                return
            
            point = int(res['result'][0]), int(res['result'][1])
            #idx = util.findImg(self.answers, answer)
            #print("=====Find Answer!=====", idx)
            #self.tapAnswer(idx)
            print("======find answer======", point[0], point[1])
            self.tapPosition(point[0], point[1])
            time.sleep(1) #skip the middle status: right answer but wrong sign
            #self.captureAnswer()

    def tapPosition(self, x, y):
        self.phone.tap(x, y, paras.SCALE)    

    def tapAnswer(self, idx):
        if idx+1 >= len(self.peaks):
            return
        bi, ei = self.peaks[idx + 1]
        self.phone.tap(int(self.w/2), int((bi+ei)/2), paras.SCALE)

    def captureAnswer(self):
        capturePath = "inputs/a0.png"
        self.phone.screencast(capturePath, paras.SCALE)
        imgAnswer = cv2.imread(capturePath)
        answerColor = [61, 192, 118]
        
        mindis, minidx = -1, 1
        for pi in range(1, len(self.peaks)):
            b, e = self.peaks[pi]
            s, n = 0, 0
            for i in range(b, e):
                for j in range(0, self.w):
                    cp = imgAnswer[i, j]
                    dis = util.dis(answerColor, cp)
                    s += dis
                    n += 1
            s /= n
            if mindis < 0 or mindis > s:
                mindis, minidx = s, pi
        
        self.store.add(self.problem, self.answers[minidx - 1])



if __name__ == "__main__" :
    pb = ProblemHandler("inputs/a0.png", None, None)
    pb.imgSrc = cv2.imread("inputs/a0.png")    
    pb.captureAnswer()


