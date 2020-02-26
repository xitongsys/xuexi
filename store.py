import os,sys,math
import util
import cv2


class Store:
    def __init__(self, path):
        self.path = path
        self.problems = []
        self.answers = []

    def find(self, problem):
        idx = util.findImg(self.problems, problem)
        if idx < 0:
            return None
        return self.answers[idx]
    
    def add(self, problem, answer):
        idx = util.findImg(self.problems, problem)
        if idx < 0:
            self.problems.append(problem)
            self.answers.append(answer)
        else:
            self.answers[idx] = answer

    def persist(self):
        for i in range(0, len(self.answers)):
            pathAnswer = os.path.join(self.path, "answer_{:06d}".format(i))
            pathProblem = os.path.join(self.path, "problem_{:06d}".format(i))
            cv2.imwrite(pathProblem, self.problems[i])
            cv2.imwrite(pathAnswer, self.answers[i])

    def load(self):
        pass