import os,sys,math

def findPeaks(data, maxInterval, threshold = 50):
    res = []
    ln = len(data)
    i = 0
    while i < ln:
        b = i
        while b < ln and data[b] < threshold:
            b += 1

        i, j = b, b
        while i < ln:
            if data[i] >= threshold:
                i, j = i + 1, i
            elif i - j < maxInterval:
                i += 1
            else:
                break
        if b < ln and j - b > 5:
            res.append([b, j])
    return res


