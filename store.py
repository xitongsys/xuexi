import os,sys,math
import util


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
        pass

    def load(self):
        pass