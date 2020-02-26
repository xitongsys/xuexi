import time
import problem, store, phone, handler

store = store.Store("./store")
phone = phone.Phone()
entryHandler = handler.Handler("pics/entrySign.jpg", phone)
endHandler = handler.Handler("pics/endSign.jpg", phone)
retryHandler = handler.Handler("pics/retrySign.jpg", phone)
problemHandler = problem.ProblemHandler("pics/problemSign.jpg", phone, store)

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
        elif problemHandler.check(inputFile):
            problemHandler.handle()
            
        else:
            time.sleep(1)
    

    