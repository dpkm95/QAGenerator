from pymongo import MongoClient as mc
db = mc("localhost", 27125)['learner']
def insertTriple(id1, id2, id3):
    triple = {"actors":list(id1), "action":id2, "objects":list(id3)}
insertTriple(eval(input()), eval(input()), eval(input()))