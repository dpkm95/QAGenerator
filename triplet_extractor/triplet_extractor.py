import os
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordPOSTagger
from nltk import PorterStemmer

#parser api link - http://www.nltk.org/api/nltk.parse.html
#nltk tree api link - http://www.nltk.org/_modules/nltk/tree.html

#set java.exe path
os.environ['JAVAHOME'] =  os.getcwd()+'\\java.exe'

#set parser environment variables
os.environ['STANFORD_PARSER'] = os.getcwd() + '\\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = os.getcwd() + '\\stanford-parser-3.5.2-models.jar'
parser = StanfordParser(model_path = os.getcwd() + '\\englishPCFG.ser')

stemmer = PorterStemmer()

noun_tags = ['NN','NNP','NNS','NNPS']
verb_tags = ['VB','VBD','VBG','VBP','VBZ','VBN']
adjective_tags = ['JJ','JJR','JJS']

def find_actor(tree):
	# tagged_line = tree[0].pos()
	print(tree.label())
	# print(tagged_line)
	# exit(0)
	# for word,tag in tagged_line:
	# 	if tag in noun_tags:
	# 		return {
	# 			'name': word,
	# 			'tag' : tag
	# 		}

def find_attributes(tree):
	pass

def get_tree(tree, tags):
	if tree.height() == 2:
		if tree.label() in tags:
			return tree
		else:
			return None
	else:
		tmp = None
		for st in tree:
			tmp = get_tree(st, tags)
			if tmp is not None:
				return tmp

def find_object(tree):
	tree = list(tree)
	st_NP = None
	st_PP = None
	st_ADJP = None
	obj_tree = None
	obj = []
	for subtree in tree[0][0][1]:
		if subtree.label() == 'NP':
			st_NP = subtree
			obj_tree = subtree
			# obj_tree = get_tree(subtree, noun_tags)
			return get_tree(subtree, noun_tags)[0]
		elif subtree.label() == 'PP':
			st_PP = subtree
			# obj_tree = get_tree(subtree, noun_tags)
			return get_tree(subtree, noun_tags)[0]
		elif subtree.label() == 'ADJP':
			st_ADJP = subtree
			# obj_tree = get_tree(subtree, noun_tags)
			return get_tree(subtree, adjective_tags)[0]
	# return obj_tree.label()
	# return find_attributes(obj_tree)

def find_predicate(tree):
	tagged_line = tree[0].pos()
	for word,tag in tagged_line[::-1]:
		if tag in verb_tags:
			return stemmer.stem(word)

def find_actor_action_prep(input_line):
	parse_tree = list(parser.parse(input_line.split()))
	# return {
	# 	'SUBJECT' : find_subject(parse_tree),
	# 	'OBJECT' : find_object(parser.parse(input_line.split())),
	# 	'PREDICATE' : find_predicate(parse_tree)
	# }
	return {
		'actor' : find_actor(parse_tree)
	}

input_line = 'The big brown dog barked at the yellow tree'
sop = find_actor_action_prep(input_line)
print(sop)