import os,sys,math
import cv2
import util

class Phone:
    def __init__(self):
        pass

    def screencast(self, name, scale):
        os.system("adb shell screencap /sdcard/a.png")
        tmpName = name + "tmp.png"
        os.system("adb pull /sdcard/a.png " + tmpName)
        img = cv2.imread(tmpName)
        img = util.resizeToGrayImg(img, scale)
        cv2.imwrite(name, img)
        

    def tap(self, x, y, scale):
        os.system("adb shell input tap {} {}".format(int(x/scale), int(y/scale)))

if __name__ == '__main__':
    phone = Phone()
    phone.screencast("inputs/a.png", 0.5)