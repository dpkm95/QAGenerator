import json
from db_helper import *
from definitions import *
import grammar_helper as gh
import gen

ACTOR_TAG = "actor"
ACTOR_ADJ_TAG = "adj"
ACTION_ADV_TAG = "adv"
ACTION_TAG = "action"
ACTION_PREP_TAG = "prep"
ACTEE_ADJ_TAG = "adj"

PREP_NAME_TAG = "name"
PREP_ACTEE_TAG = "actee"

VALID_PREP = ["","aboard","about","above","across","after","against","along","amid","among","anti","around","as","at",
              "before","behind","below","beneath","beside","besides","between","beyond","but","by","concerning",
              "considering","despite","down","during","except","excepting","excluding","following","for","from","in",
              "inside","into","like","minus","near","of","off","on","onto","opposite","outside","over","past","per",
              "plus","regarding","round","save","since","than","through","to","toward","towards","under","underneath",
              "unlike","until","up","upon","versus","via","with","within","without" ]



def get_actor(base):
    return base[ACTOR_TAG]


def get_action(actor):
    return actor[ACTION_TAG]


def normalize_and_insert_actor(actor):
    actor[KEY_NAME] = actor[KEY_NAME][0] # assuming only one actor
    actor[KEY_NAME] = actor[KEY_NAME].lower()
    del actor[ACTION_TAG]
    actor[KEY_ATTR] = actor[ACTOR_ADJ_TAG]
    del actor[ACTOR_ADJ_TAG]
    return DbHelper.insert_actor_or_actee(actor)


def normalize_and_insert_actee(actee):
    actee[KEY_NAME] = actee[KEY_NAME][0] # assuming only one actee
    actee[KEY_NAME] = actee[KEY_NAME].lower()
    actee[KEY_ATTR] = actee[ACTEE_ADJ_TAG]
    del actee[ACTEE_ADJ_TAG]
    return DbHelper.insert_actor_or_actee(actee)


def normalize_and_insert_action(action, actor_inserted):
    action[KEY_ATTR] = action[ACTION_ADV_TAG]
    del action[ACTION_ADV_TAG]
    del action[ACTOR_ADJ_TAG]
    action[KEY_ACTORS] = [actor_inserted[KEY_ID]]
    valid_preps = []
    if action[KEY_NAME] == "is":
        preps = action[ACTION_PREP_TAG]
        if len(preps) == 0:
            # ignore, side-effect of a sentence like "Rose is brave", adjective already associated with actor
            return None
        if len(list(filter(lambda x: x[KEY_NAME]!="", action[ACTION_PREP_TAG]))) == 0:
            # special case -> super class has been defined
            # TODO: Look into super class and is-as-an-action being defined with same is - even possible?
            for prep in action[ACTION_PREP_TAG]:
                actee_inserted = normalize_and_insert_actee(prep[PREP_ACTEE_TAG])
                add_super_type(actor_inserted, get_type_resolved(actee_inserted))
            return None

    for prep in action[ACTION_PREP_TAG]:
        # if not prep[PREP_NAME_TAG] in VALID_PREP: continue
        actee = prep[PREP_ACTEE_TAG]
        actee_inserted_id = get_id(normalize_and_insert_actee(actee))
        prep[PREP_ACTEE_TAG] = [actee_inserted_id]
        valid_preps.append(prep)
    action[ACTION_PREP_TAG] = valid_preps
    return DbHelper.insert_action(action)


def insert_into_db(base):
    actor = get_actor(base)

    action = get_action(actor)  # this needs to happen before normalization

    inserted_actor = normalize_and_insert_actor(actor)
    #print(actor)
    normalize_and_insert_action(action, inserted_actor)  # handles insertion of respective actees also
    #print(action)


def parse_input():
    with open(input()) as f:
        lines = list(map(lambda x: x.strip(), f.readlines()))

    for i in lines:
        base = json.loads(i)
        insert_into_db(base)

    #for i in DbHelper.entities:
    #   print(i)

    gen.show_qs()

if __name__ == "__main__":
    parse_input()