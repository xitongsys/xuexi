import handler
import phone

phone = phone.Phone()
entryHandler = handler.Handler("pics/entrySign.jpg", phone)

if __name__ == '__main__':
    phone.screencast("inputs/a.png")
    if entryHandler.check("inputs/a.png"):
        entryHandler.handle()
    