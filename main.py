import handler
import phone
import time

phone = phone.Phone()
entryHandler = handler.Handler("pics/entrySign.jpg", phone)
endHandler = handler.Handler("pics/endSign.jpg", phone)
retryHandler = handler.Handler("pics/retrySign.jpg", phone)

inputFile = "inputs/a.png"

if __name__ == '__main__':
    while True:
        phone.screencast(inputFile)
        if entryHandler.check(inputFile):
            entryHandler.handle()
        elif endHandler.check(inputFile):
            endHandler.handle()
        elif retryHandler.check(inputFile):
            retryHandler.handle()
        else:
            time.sleep(1)
    

    