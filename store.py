import os,sys,math
import util
import cv2


class Store:
    def __init__(self, path):
        self.path = path
        self.problems = []
        self.answers = []
        self.load()

    def find(self, problem):
        idx = util.findImg(self.problems, problem)
        if idx < 0:
            return None
        print("store find ", idx)
        return self.answers[idx]
    
    def add(self, problem, answer):
        idx = util.findImg(self.problems, problem)
        if idx < 0:
            self.problems.append(problem)
            self.answers.append(answer)
            idx = len(self.answers) - 1
        else:
            self.answers[idx] = answer
        self.persist(idx)

    def persist(self, idx):
            pathAnswer = os.path.join(self.path, "{:06d}_answer.jpg".format(idx))
            pathProblem = os.path.join(self.path, "{:06d}_problem.jpg".format(idx))
            cv2.imwrite(pathProblem, self.problems[idx])
            cv2.imwrite(pathAnswer, self.answers[idx])

    def load(self):
        pics = []
        for f in os.listdir(self.path):
            pf = os.path.join(self.path, f)
            if os.path.isfile(pf):
                pics.append(pf)
        pics.sort()
        num = len(pics)
        for i in range(0, num, 2):
            pathAnswer, pathProblem = pics[i], pics[i+1]
            self.answers.append(cv2.imread(pathAnswer))
            self.problems.append(cv2.imread(pathProblem))
