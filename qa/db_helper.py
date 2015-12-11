from definitions import *
import undependent_grammar_helper as ugh

class DbHelper():
    # establish conn TODO
    # db = mc("localhost", 27125)['learner']
    # objs = db['objs']
    # temp for demonstration
    dogClass = {"_id": 'ObjectId("5617b2fb5632c6d04dc9edca")', "name": "dog", "tag": "NN", "class": True}
    dog = {"_id": 'ObjectId("5617b3305632c6d04dc9edcb")', "name": "dog", "type": 'ObjectId("5617b2fb5632c6d04dc9edca")',
           "attr": [], "tag": "NN"}
    # John is old. John is a person.
    personClass = {"_id": "9", "name": "person", "tag": "NN", "class": True}
    person = {"_id": '8', "name": "person", "tag": "NN", "type": "9"}
    johnClass = {"_id": '7', "name": "John", "tag": "NNP", "class": True, "type": "8"}
    john = {"_id": 'ObjectId("3")', "name": "John", "attr": ['ObjectId("2")'], "tag": "NNP", "type": "7"}
    # The tree is yellow, old and brown. Yellow is a color. Brown is a color.
    colorClass = {"_id": "0", "name": "colour", "class": True, "tag": "NN"}
    color = {"_id": "1", "name": "colour", "tag": "NN", "type": "0"}  # NN appropriate??? TODO
    yellowClass = {"_id": '2', "name": "yellow", "tag": "JJ", "type": "1", "class": True}
    yellow = {"_id": 'ObjectId("5617b3565632c6d04dc9edcc")', "name": "yellow", "tag": "JJ", "type": "2"}
    brown = {"_id": 'ObjectId("1")', "name": "brown", "tag": "JJ", "type": "3"}
    brownClass = {"_id": '3', "name": "brown", "tag": "JJ", "type": "1", "class": True}
    old = {"_id": 'ObjectId("2")', "name": "old", "tag": "JJ"}
    treeClass = {"_id": 'ObjectId("5617b3715632c6d04dc9edcd")', "name": "tree", "tag": "NN", "class": True}
    tree = {"_id": 'ObjectId("5618bc70c937ac93946f9325")', "name": "tree", "tag": "NN",
            "type": 'ObjectId("5617b3715632c6d04dc9edcd")',
            "attr": ['ObjectId("5617b3565632c6d04dc9edcc")', 'ObjectId("1")', 'ObjectId("2")']}

    # barkClass = {"_id":'ObjectId("56asa23131231asd2231")', "name":"bark", "class":True}
    # bark = { "_id" : 'ObjectId("5618c2e3c937ac93946f9326")', "name" : "bark", "tag" : "VBD",
    # "actors" : [  {  "_id" : 'ObjectId("5617b3305632c6d04dc9edcb")' } ], "prep":{"at":['ObjectId("5618bc70c937ac93946f9325")']} }

    age = {"_id": '5', "name": "age", "tag": "JJ", "type": "6"}
    ageClass = {"_id": '6', "name": "age", "tag": "JJ", "class": True}

    entities = []
    temp_entities = [dog, dogClass, tree, treeClass, yellow, yellowClass, brown, brownClass,
                     old, age, ageClass, john, johnClass, person, personClass, color, colorClass]

    st1_entities = [

    ]
    next_id = 1

    @staticmethod
    def create_set_own_type(entity): # the initial type creation for an entity
        type_entity = {KEY_NAME: entity[KEY_NAME], KEY_ID: DbHelper.next_id, KEY_CLASS:True, KEY_TAG:entity[KEY_TAG]}
        DbHelper.next_id += 1
        DbHelper.entities.append(type_entity)
        set_type(entity, type_entity[KEY_ID])

    @staticmethod
    def insert_attrs(raw_attrs):
        for raw in raw_attrs:
            existing_entities = get_instance_entities_with(KEY_NAME, get_name(raw)) # only max 1 may exist in current system
            if len(existing_entities) == 0:
                # new attribute
                raw[KEY_ID] = DbHelper.next_id
                DbHelper.next_id += 1
                DbHelper.entities.append(raw)
                DbHelper.create_set_own_type(raw)
            else: # already exists, as an adjective or a noun
                set_id(raw, get_id(existing_entities[0]))
                # if it was a noun earlier, make it an adjective now
                set_tag(existing_entities[0], get_tag(raw))
                # TODO: What about different kinds of adjectives overriding each other?
                # TODO: Support of abstract nouns should change this overriding

        return list(map(get_id, raw_attrs))

    @staticmethod
    def insert_actor_or_actee(entity):
        existing_entities = get_instance_entities_with(KEY_NAME, entity[KEY_NAME])
        if len(existing_entities) == 0:
            entity[KEY_ID] = DbHelper.next_id
            DbHelper.next_id += 1
            entity[KEY_ATTR] = DbHelper.insert_attrs(entity[KEY_ATTR])
            DbHelper.entities.append(entity)
            DbHelper.create_set_own_type(entity)
            return entity
        else:
            existing_attrs = get_attrs_resolved(existing_entities[0])
            new_attrs = []
            for attr in entity[KEY_ATTR]:
                if attr[KEY_NAME] not in list(map(get_name, existing_attrs)):
                    new_attrs.append(attr)
            add_to_attrs(existing_entities[0], DbHelper.insert_attrs(new_attrs))
            return existing_entities[0]

    @staticmethod
    def insert_action(action_entity):
        # every action entering should be a new action since an action cannot be repeated as of now
        # repetition will occur when we include references (the boy who attacked), though this will probably involve
        # a query system too, and "the boy who killed" will entirely be resolved to a single entity (referenced boy)
        # only "boy who brutally killed" may end up adding attributes to the existing function
        action_entity[KEY_ID] = DbHelper.next_id
        DbHelper.next_id += 1
        action_entity[KEY_ATTR] = DbHelper.insert_attrs(action_entity[KEY_ATTR])
        DbHelper.entities.append(action_entity)
        return action_entity

    @staticmethod
    def merge_entity(entity):
        pass  # TODO:

    def __init__(self):
        pass  # any setup if required such as establishing data connection to db, allow creation of multiple for
        # representing multiple data banks

    @staticmethod
    def resolve(_id):
        # implement a cache to prevent creation of multiple references (think this applies to when we actually use db)
        try:
            return next(i for i in DbHelper.entities if get_id(i) == _id)
        except StopIteration:
            raise Exception("DbHelper: Could not find " + str(_id) + " in database!")


def _get_entities_in(entity, key):
    '''
    :param entity: entity with some list of objectIds which are to be dereferenced
    :param key: entity[key] is used to access the list of objectIds to dereference
    :return: list of dereferenced entities
    '''
    dereferenced_entities = []
    if key not in entity:
        return []
    for i in entity[key]:
        dereferenced_entities.append(DbHelper.resolve(i))

    return dereferenced_entities


def get_instance_entities_with(key, value):
    return [i for i in DbHelper.entities if i[key] == value and not is_class(i)]


def get_all_actions_resolved():
    return [i for i in DbHelper.entities if ugh.is_verb(get_tag(i))]

def get_actions_by(actor_entity):
    return [i for i in DbHelper.entities if ugh.is_verb(i) and get_id(actor_entity) in get_actors(i)]


def get_actors(action_entity):
    return action_entity[KEY_ACTORS]


def get_actees(prep):
    return prep[KEY_ACTEES]


def get_actees_resolved(prep):
    return [DbHelper.resolve(i) for i in get_actees(prep)]


def get_actors_resolved(action_entity):
    return [DbHelper.resolve(i) for i in get_actors(action_entity)]


def get_preps(action_entity):
    return action_entity[KEY_PREP]


def get_class(entity):
    type = get_type(entity)
    return DbHelper.resolve(type) if type is not None else None


# these get_<key> type functions are meant to be used instead of direct dictionary access in case we decide to accomodate
# some sort of inheritance etc. Or should it be done by resolve? Either way no harm.

def get_id(entity):
    return entity[KEY_ID]


def get_name(entity):
    return entity[KEY_NAME]


def get_tag(entity):
    return entity[KEY_TAG]


def get_type(entity):
    return None if KEY_TYPE not in entity else entity[KEY_TYPE]


def is_class(entity):
    return KEY_CLASS in entity and entity[KEY_CLASS] == True  # defensive


def get_type_resolved(entity):
    return None if KEY_TYPE not in entity else DbHelper.resolve(entity[KEY_TYPE])


def get_super_type_resolved(entity):
    '''
    A super type is not just an object's type (class), it is the class of its class. The super type of a yellow object
    is the type of the type i.e the type(type(yellow)) i.e type(yellow class)
    :param entity:
    :return:
    '''
    ctr = 0
    while entity is not None:
        if is_class(entity):
            if ctr == 1: return entity
            ctr += 1
        entity = get_type_resolved(entity)
    return None


def get_attrs(entity):
    return [] if KEY_ATTR not in entity else entity[KEY_ATTR]


def get_attrs_resolved(entity):
    return _get_entities_in(entity, KEY_ATTR)


def get_actions(entity):
    return _get_entities_in(entity, KEY_ACTIONS)


def set_type(entity, type_id):
    entity[KEY_TYPE] = type_id


def set_tag(entity, tag):
    entity[KEY_TAG] = tag


def set_id(entity, id):
    entity[KEY_ID] = id


def add_super_type(entity, super_type):
    if not is_class(super_type): raise AssertionError("Super type must be a type!")
    set_type(get_type_resolved(entity), super_type[KEY_ID])


def add_to_attrs(entity, attr_ids):
    old_attrs = get_attrs(entity)
    old_attrs.extend(attr_ids)
    entity[KEY_ATTR] = old_attrs