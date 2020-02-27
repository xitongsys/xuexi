import os,sys,math
import aircv as ac
import util, paras

class Handler:
    def __init__(self, name, imgSign, phone):
        self.imgSign = ac.imread(imgSign)
        self.point = []
        self.phone = phone
        self.name = name

    def check(self, imgSrc) -> bool:
        self.imgSrc = ac.imread(imgSrc)
        res = util.match(self.imgSrc, self.imgSign)
        # print(res)
        if res != None :
            self.point = [int(res['result'][0]), int(res['result'][1])]
            return True
        return False
    
    def handle(self):
        print("handle ", self.name)
        self.phone.tap(self.point[0], self.point[1], paras.SCALE)
        
