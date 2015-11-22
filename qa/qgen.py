from db_helper import *
import sentence_builder as sb
import grammar_helper as gh


def getGeneralQ(entity):
    '''
    :param entity: assumed to be resolved and have 1 or more attributes
    :return: a single question,answer pair such as "Describe the <entity name>"
    '''
    attr_names = list(map(get_name, get_attrs(entity)))
    q = " ".join(["Describe", sb.get_qualified_noun_name(entity)]) + "."
    a = " ".join([sb.get_qualified_noun_name(entity), "is", sb.combine_with_comma_and(attr_names)]).capitalize() + "."
    points = len(attr_names)
    return [q, a, points]


def get_specific_q(entity, attr_type, attrs):
    '''
    Assumes attr has a super class i.e a "type"
    :param attr:
    :param entity:
    :return:
    '''
    attr_names = map(get_name, attrs)
    attr_type_name = get_name(attr_type)
    entity_name = get_name(entity)
    # TODO: Consider and decide on whether to use "What colour is the tree" instead of "What is the colour of tree"
    if gh.is_proper_noun(entity):
        # ASSUMPTION: all proper nouns should be "possessive" of their attributes. Giggle.
        q = " ".join(["What is", sb.get_possessive(entity_name), attr_type_name]) + "?"
        a = " ".join([sb.get_possessive(entity_name), attr_type_name, "is", sb.combine_with_comma_and(attr_names)]) + "."
    else:
        q = " ".join(["What is the", attr_type_name, "of", "the", entity_name]) + "?"
        a = " ".join(["The", attr_type_name, "of the", entity_name, "is", sb.combine_with_comma_and(attr_names)]) + "."
    points = len(attrs)
    return [q, a, points]


def gen_attr_question(entity):
    ql = []
    if len(get_attrs(entity)) == 0: # no attributes, no questions
        return ql
    # if we have even one attribute, we can ask the "describe" question
    ql.append(getGeneralQ(entity))

    # generate question specific to the type of the attribute, if present. attributes without a "type" will be ignored.
    done_attrs = []
    attrs = get_attrs(entity)
    for attr in attrs:
        super_type = get_super_type(attr)
        if not super_type is None and attr not in done_attrs: # this will need to be changed when we support multiple types, since we can revisit done attrs for different super classes
            done_attrs.append(attr)
            common_attrs = [attr]
            for j in [DbHelper.resolve(_) for _ in set(map(get_id, attrs)) - set(map(get_id, done_attrs))]:
                if get_super_type(j) == super_type:
                    done_attrs.append(j)
                    common_attrs.append(j)

            ql.append(get_specific_q(entity, super_type, common_attrs))

    return ql


def gen_type_question(entity): # questions based on the type (superclass) of an entity, if possible
    ql = []
    super_type = get_super_type(entity)
    if not super_type is None:
        q = "What is " + sb.get_qualified_noun_name(entity) + "?"
        a = get_name(entity) + " is a " + get_name(super_type) + "."
        points = 1
        ql.append([q,a,points])
    return ql

def gen_all_questions(entity):
    ql = gen_attr_question(entity)
    ql.extend(gen_type_question(entity))
    for i in ql:
        i[0] = i[0].capitalize()
        i[1] = i[1].capitalize()
    return ql
