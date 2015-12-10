from definitions import *

def is_verb(entity_tag):
    return entity_tag in [TAG_VB, TAG_VBD, TAG_VBG, TAG_VBN, TAG_VBP, TAG_VBZ]