import os,json
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordPOSTagger
# from nltk import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

#parser api link - http://www.nltk.org/api/nltk.parse.html
#nltk tree api link - http://www.nltk.org/_modules/nltk/tree.html

# #linux version
# #set java.exe path
# os.environ['JAVAHOME'] =  os.getcwd()+'/java'

# #set parser environment variables
os.environ['STANFORD_PARSER'] = os.getcwd() + '/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = os.getcwd() + '/stanford-parser-3.5.2-models.jar'
parser = StanfordParser(model_path = os.getcwd()+'/englishFactored.ser.gz')

#windows version
#os.environ['JAVAHOME'] =  os.getcwd()+'\\java.exe'

#set parser environment variables
#os.environ['STANFORD_PARSER'] = os.getcwd() + '\\stanford-parser.jar'
#os.environ['STANFORD_MODELS'] = os.getcwd() + '\\stanford-parser-3.5.2-models.jar'
#parser = StanfordParser(model_path = os.getcwd() + '\\englishFactored.ser.gz')

# stemmer = PorterStemmer()
stemmer = SnowballStemmer("english")

noun_tags = ['NN','NNP','NNS','NNPS']
verb_tags = ['VB','VBD','VBG','VBP','VBZ','VBN']
adjective_tags = ['JJ','JJR','JJS']
adverb_tags = ['RB','RBR','RBS']

def get_actor(tree):
	adj = []
	actor = {}
	#to catch NNP
	prev_tag = None
	name_value = ""
	for subtree in tree.subtrees():
		if subtree.label() in adjective_tags:
			adj.append({
					'name' : subtree[0],
					'tag' : subtree.label() 
				})		
		if prev_tag == 'NNP' or subtree.label() == 'NNP':
			name_value += subtree[0]+" "
		else:
			if subtree.label() in noun_tags:
				actor['name'] = subtree[0],
				actor['tag'] = subtree.label()
		prev_tag = subtree.label()
	if name_value != "":
		actor['name'] = name_value.strip(),
		actor['tag'] = 'NNP'
	# if len(adj) != 0:
	actor['adj']=adj
	return actor

def get_action(tree):
	action = {}
	adv = []
	adj = []
	prep = []
	for subtree in tree[1]:
		if subtree.label() in verb_tags:
			if subtree[0] == 'was':
				action['name'] = 'is'
			else:
				action['name'] = subtree[0]
			action['tag'] = subtree.label()
		elif subtree.label() == 'ADJP':
			for st in subtree.subtrees():
				if st.label() in adjective_tags:
					adj.append({'name':st[0],'tag':st.label()})
		elif subtree.label() == 'ADVP':
			for st in subtree.subtrees():
				if st.label() in adverb_tags:
					adv.append({'name':st[0],'tag':st.label()})
		elif subtree.label() == 'NP':
			# new_prep = {'name':subtree[0][0]}
			new_prep = {'name':""}
			new_prep['actee'] = get_actor(subtree)
			prep.append(new_prep)
		elif subtree.label() == 'PP':
			new_prep = {'name':subtree[0][0]}
			if subtree[1].label() == 'NP':
				new_prep['actee'] = get_actor(subtree[1])
			prep.append(new_prep)
	action['prep'] = prep
	# if len(adv) != 0:
	action['adv'] = adv	
	# if len(adj) != 0:
	action['adj'] = adj
	return action

def find_subject_object_predicate(input_line):
	input_line = input_line.strip()
	input_line = input_line.replace('.','')
	parse_tree = parser.parse(input_line.split())
	parse_tree_clone = list(parse_tree)[0].copy()
	actor = get_actor(parse_tree_clone[0][0])
	actor['action'] = get_action(parse_tree_clone[0])
	return {
		'actor' : actor
	}

# Little Red Riding Hood is a girl.
# Little Red Riding Hood went to the woods.
# The big bad wolf was in the woods.
# Grandma slept at home.
# The big bad wolf ate Grandma.
# The big bad wolf hid under the blanket.
# The Woodsman killed the big bad wolf.
# The Woodsman threw the big bad wolf in the river.
# Little Red Riding Hood thanked the Woodsman.
while True:
    input_line = raw_input()
    if input_line == "generate": break
    sop = find_subject_object_predicate(input_line)
    print(json.dumps(sop))

