from db_helper import *
import sentence_builder as sb
import grammar_helper as gh


def getGeneralQ(entity):
    '''
    :param entity: assumed to be resolved and have 1 or more attributes
    :return: a single question,answer pair such as "Describe the <entity name>"
    '''
    attr_names = list(map(get_name, get_attrs_resolved(entity)))
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
        a = " ".join(
            [sb.get_possessive(entity_name), attr_type_name, "is", sb.combine_with_comma_and(attr_names)]) + "."
    else:
        q = " ".join(["What is the", attr_type_name, "of", "the", entity_name]) + "?"
        a = " ".join(["The", attr_type_name, "of the", entity_name, "is", sb.combine_with_comma_and(attr_names)]) + "."
    points = len(attrs)
    return [q, a, points]


def gen_attr_question(entity):
    ql = []
    if len(get_attrs_resolved(entity)) == 0:  # no attributes, no questions
        return ql
    # if we have even one attribute, we can ask the "describe" question
    ql.append(getGeneralQ(entity))

    # generate question specific to the type of the attribute, if present. attributes without a "type" will be ignored.
    done_attrs = []
    attrs = get_attrs_resolved(entity)
    for attr in attrs:
        super_type = get_super_type_resolved(attr)
        if not super_type is None and attr not in done_attrs:  # this will need to be changed when we support multiple types, since we can revisit done attrs for different super classes
            done_attrs.append(attr)
            common_attrs = [attr]
            for j in [DbHelper.resolve(_) for _ in set(map(get_id, attrs)) - set(map(get_id, done_attrs))]:
                if get_super_type_resolved(j) == super_type:
                    done_attrs.append(j)
                    common_attrs.append(j)

            ql.append(get_specific_q(entity, super_type, common_attrs))

    return ql


def gen_type_question(entity):  # questions based on the type (superclass) of an entity, if possible
    ql = []
    super_type = get_super_type_resolved(entity)
    if not super_type is None:
        q = "What is " + sb.get_qualified_noun_name(entity) + "?"
        a = sb.get_qualified_noun_name(entity) + " is a " + get_name(super_type) + "."
        points = 1
        ql.append([q, a, points])
    return ql


def gen_action_q_xpp(action):
    # Who did action to actee?
    # TODO: Add support for multiple actors and actees
    actor = get_actors_resolved(action)[0]
    preps = get_preps(action)
    parts = [
        sb.get_appropriate_interrogative_for_noun(actor, True),
        get_name(action)
    ]
    actees = []
    if len(preps) == 0:  # Grandma slept.
        pass
    elif get_name(preps[0]) != "":
        parts.append(get_name(preps[0]))
        actees = get_actees_resolved(preps[0])
    else:
        actees = get_actees_resolved(preps[0])

    if len(actees) != 0:
        parts.append(sb.combine_with_comma_and(map(sb.get_qualified_noun_name, actees)))

    q = " ".join(parts) + "?"
    # the answer
    parts[0] = sb.get_qualified_noun_name(actor)
    a = " ".join(parts) + "."
    points = 1  # TODO: Change when multiple actor support added
    return [[q, a, points]]


def gen_action_q_ppx(action):
    # actor did action to what?
    # TODO: Add support for multiple actors and actees
    actor = get_actors_resolved(action)[0]
    preps = get_preps(action)
    parts = [
        sb.get_qualified_noun_name(actor),
        get_name(action)
    ]
    actees = []
    if len(preps) == 0:  # Grandma slept.
        return []
    elif get_name(preps[0]) != "":
        parts.append(get_name(preps[0]))
        actees = get_actees_resolved(preps[0])
    else:
        actees = get_actees_resolved(preps[0])

    if len(actees) == 0:
        return []
    parts.append(sb.get_appropriate_interrogative_for_noun(actees[0], False)) # TODO: Modify to allow "what and whom" simultaneously

    q = " ".join(parts) + "?"
    # the answer
    # TODO: Change points when multiple actor support added
    parts[-1], points = sb.get_fully_qualified_descriptive_name_with_marks(actees[0])
    a = " ".join(parts) + "."
    return [[q, a, points]]


def gen_action_question(entity):
    ql = []
    for action in get_all_actions_resolved():
        ql.extend(gen_action_q_xpp(action))
        ql.extend(gen_action_q_ppx(action))
    return ql


def gen_all_questions(entity):
    ql = gen_attr_question(entity)
    ql.extend(gen_type_question(entity))
    ql.extend(gen_action_question(entity))  # TODO: not here!
    for i in ql:
        i[0] = i[0][0].capitalize() + i[0][1:]
        i[1] = i[1][0].capitalize() + i[1][1:]
    return ql
