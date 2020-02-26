import os,sys,math

class Phone:
    def __init__(self):
        pass

    def screencast(self, name):
        os.system("adb shell screencap /sdcard/a.png")
        os.system("adb pull /sdcard/a.png " + name)
        

    def tap(self, x, y):
        os.system("adb shell input tap {} {}".format(x, y))