import os,sys,math
import aircv as ac

class Handler:
    def __init__(self, imgSign, phone):
        self.imgSign = ac.imread(imgSign)
        self.point = []
        self.phone = phone

    def check(self, imgSrc) -> bool:
        self.imgSrc = ac.imread(imgSrc)
        res = ac.find_template(self.imgSrc, self.imgSign, 0.5)
        print(res)
        if res != None :
            self.point = [int(res['result'][0]), int(res['result'][1])]
            return True
        return False
    
    def handle(self):
        self.phone.tap(self.point[0], self.point[1])
        
