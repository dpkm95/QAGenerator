import qgen
import sentence_builder as sb
from db_helper import *
import grammar_helper as gh

# The tree is yellow, old and brown.
yellowClass = {"_id": '2', "name": "yellow", "tag": "JJ", "class": True}
yellow = {"_id": 'ObjectId("5617b3565632c6d04dc9edcc")', "name": "yellow", "tag": "JJ", "type": "2"}
brown = {"_id": 'ObjectId("1")', "name": "brown", "tag": "JJ", "type": "3"}
brownClass = {"_id": '3', "name": "brown", "tag": "JJ", "class": True}
old = {"_id": 'ObjectId("2")', "name": "old", "tag": "JJ"}
treeClass = {"_id": 'ObjectId("5617b3715632c6d04dc9edcd")', "name": "tree", "tag": "NN", "class": True}
tree = {"_id": 'ObjectId("5618bc70c937ac93946f9325")', "name": "tree", "tag": "NN",
        "type": 'ObjectId("5617b3715632c6d04dc9edcd")',
        "attr": ['ObjectId("5617b3565632c6d04dc9edcc")', 'ObjectId("1")', 'ObjectId("2")']}

set1 = [yellowClass, yellow, brown, brownClass, treeClass, tree, old]

# Yellow is a color.
colorClass = {"_id": "0", "name": "colour", "class": True, "tag": "NN"}
color = {"_id": "1", "name": "colour", "tag": "NN", "type": "0"}
yellowClass = {"_id": '2', "name": "yellow", "tag": "JJ", "class": True, "type": "1"}

set2 = [yellowClass, yellow, brown, brownClass, treeClass, tree, color, colorClass, old]

# Brown is a color
brown = { "_id" : 'ObjectId("1")', "name" : "brown", "tag" : "JJ", "type":"3" }
brownClass = { "_id" : '3', "name" : "brown", "tag" : "JJ", "type":"1", "class":True }

set3 = [yellowClass, yellow, brown, brownClass, treeClass, tree, color, colorClass, old]

all_sets = [("The tree is yellow, old and brown.", set1), ("Yellow is a color.", set2), ("Brown is a color.", set3)]

DbHelper.entities = [yellowClass, yellow, brown, brownClass, treeClass, tree]


def show_qs():
    qset = set()
    for i in [i for i in DbHelper.entities if not (is_class(i) and gh.is_proper_noun(i))]:
        for j in qgen.gen_all_questions(i):
            qset.add(tuple(j))

    for q, a, marks in qset:
        print("Q.", q)
        print("A.", a)
        print("Marks: ", marks)
        print("")

for i in all_sets:

    print(i[0])
    input()
    DbHelper.entities = i[1]
    show_qs()
    input()

# print(AttrQ.gen_all_questions(DbHelper.tree))
# print(AttrQ.gen_all_questions(DbHelper.john))
# print(get_super_type(DbHelper.yellow))
