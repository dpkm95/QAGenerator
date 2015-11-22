import grammar_helper as gh
from db_helper import *


def combine_with_comma_and(words):
    words = list(words)
    if len(words) == 1:
        return  words[0]
    elif len(words) == 2:
        return words[0] + " and " + words[1]
    else:
        return ", ".join(words[0:-1]) + " and " + words[-1]


def get_possessive(name): # assumes proper noun since common nouns are not allowed possession
    return name.capitalize() + "'" + ("" if name[-1] == 's' else "s")


def get_qualified_noun_name(entity):
    name= ''
    if gh.is_noun(entity):
        name = get_name(entity) if gh.is_proper_noun(entity) else "the " + get_name(entity)
    elif gh.is_adjective(entity):
        name = gh.get_abstract_noun_adj(entity)
    elif gh.is_verb(entity):
        name = "the " + get_name(entity)
    return name