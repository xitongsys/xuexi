import time
import problem, store, phone, handler

store = store.Store("./store")
phone = phone.Phone()
entryHandler = handler.Handler("entry", "pics/entrySign.jpg", phone)
endHandler = handler.Handler("end", "pics/endSign.jpg", phone)
retryHandler = handler.Handler("retry", "pics/retrySign.jpg", phone)
exitHandler = handler.Handler("exit", "pics/exitSign.jpg", phone)
backHandler = handler.Handler("back", "pics/backSign.jpg", phone)
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
        elif exitHandler.check(inputFile):
            exitHandler.handle()
        elif problemHandler.check(inputFile):
            problemHandler.handle()
        elif backHandler.check(inputFile):
            backHandler.handle()

        else:
            time.sleep(1)
    

    