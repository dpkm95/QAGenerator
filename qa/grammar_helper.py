from db_helper import *


def is_proper_noun(entity):
    return entity[KEY_TAG] == TAG_NNP or entity[KEY_TAG] == TAG_NNPS


def is_adjective(entity):
    return entity[KEY_TAG] in ["JJ", "JJR", "JJS"] # add or-ed expressions later if required


def is_noun(entity):
    return get_tag(entity) in [TAG_NNP, TAG_NNPS, TAG_NN, TAG_NNS]


def is_verb(entity):
    return get_tag(entity) in [TAG_VB, TAG_VBD, TAG_VBG, TAG_VBN, TAG_VBP, TAG_VBZ]


def get_verb_with_tense(entity):
    if not is_verb(entity): raise AssertionError(str(entity) + " not a verb!")
    base_name = get_name(entity)
    sw = {TAG_VBD:base_name+"ed"}
    return sw[get_tag(entity)]


def get_abstract_noun_adj(adjective_entity):
    # need magic, just return the name for now
    return get_name(adjective_entity)


def get_verb_continuous(entity):
    if not is_verb(entity): raise AssertionError(str(entity) + " not a verb!")
    return get_name(entity) + "ing"