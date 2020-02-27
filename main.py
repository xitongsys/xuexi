import time
import problem, store, phone, handler, paras

store = store.Store("./store")
phone = phone.Phone()
entryHandler = handler.Handler("entry", "pics/entrySign.jpg", phone)
endHandler = handler.Handler("end", "pics/endSign.jpg", phone)
retryHandler = handler.Handler("retry", "pics/retrySign.jpg", phone)
exitHandler = handler.Handler("exit", "pics/exitSign.jpg", phone)
backHandler = handler.Handler("back", "pics/backSign.jpg", phone)
wrongHandler = handler.Handler("wrong", "pics/wrongSign.jpg", phone)
problemHandler = problem.ProblemHandler("pics/problemSign.jpg", phone, store)

inputFile = "inputs/a.png"

if __name__ == '__main__':
    while True:
        phone.screencast(inputFile, paras.SCALE)
        if entryHandler.check(inputFile):
            entryHandler.handle()
        elif endHandler.check(inputFile):
            endHandler.handle()
        elif exitHandler.check(inputFile):
            exitHandler.handle()
        elif retryHandler.check(inputFile):
            retryHandler.handle()
        elif problemHandler.check(inputFile):
            problemHandler.handle()
        elif wrongHandler.check(inputFile):
            backHandler.check(inputFile)
            backHandler.handle()

        else:
            pass
            #time.sleep(1)
    

    