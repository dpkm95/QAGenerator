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
        name = get_name(entity).title() if gh.is_proper_noun(entity) else "the " + get_name(entity)
    elif gh.is_adjective(entity):
        name = gh.get_abstract_noun_adj(entity)
    elif gh.is_verb(entity):
        name = "the " + get_name(entity)
    return name


def get_appropriate_interrogative_for_noun(noun_entity, is_actor):
    if not gh.is_noun(noun_entity): raise AssertionError("Expected noun!")
    if gh.is_proper_noun(noun_entity):
        return "who" if is_actor else "whom"
    else:
        return "what"


# def get_prepositional_phrase(prep_name, )

def get_fully_qualified_descriptive_name_with_marks(entity_noun):
    if gh.is_proper_noun(entity_noun):
        return get_qualified_noun_name(entity_noun), 1
    else:
        attrs = get_attrs_resolved(entity_noun)
        if len(attrs) == 0:
            return get_qualified_noun_name(entity_noun), 1
        else:
            return "the " + combine_with_comma_and(map(get_name, attrs)) + " " + get_name(entity_noun), len(attrs) + 1