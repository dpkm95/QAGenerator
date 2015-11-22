import json
from db_helper import *
from definitions import *
import qgen

ACTOR_TAG = "actor"
ACTOR_ADJ_TAG = "adj"
ACTION_ADV_TAG = "adv"
ACTION_TAG = "action"
ACTEE_TAG = "actee"


def get_actor(base):
    return base[ACTOR_TAG]


def get_action(actor):
    return actor[ACTION_TAG]


def normalize_actor(actor):
    actor[KEY_NAME] = actor[KEY_NAME][0]
    del actor[ACTION_TAG]
    actor[KEY_ATTR] = actor[ACTOR_ADJ_TAG]
    del actor[ACTOR_ADJ_TAG]


def normalize_action(action, normalized_actor):
    action[KEY_ATTR] = action[ACTION_ADV_TAG]
    del action[ACTION_ADV_TAG]
    del action[ACTOR_ADJ_TAG]
    action[KEY_ACTORS] = []
    action[KEY_ACTORS].append(normalized_actor[KEY_ID])


def parse_input():
    base = json.loads(input())
    actor = get_actor(base)

    action = get_action(actor)

    normalize_actor(actor)
    print(actor)
    actor = DbHelper.insert_actor_or_actee(actor)

    normalize_action(action, actor)
    action = DbHelper.insert_action(action)
    print(action)

    # print(DbHelper.entities)
    print(qgen.gen_all_questions(actor))
    # print(qgen.gen_all_questions(action))


parse_input()