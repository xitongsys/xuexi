import aircv as ac

def match(imgSrc, imgObj, confidence=0.5):
    imgSrc = ac.imread(imgSrc)
    imgObj = ac.imread(imgObj)

    res = ac.find_template(imgSrc, imgObj, confidence)
    print(res)

if __name__ == '__main__':
    match("c.jpg", "d.jpg")