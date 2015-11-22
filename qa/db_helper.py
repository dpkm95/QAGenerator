from definitions import *

class DbHelper():
    # establish conn TODO
    #db = mc("localhost", 27125)['learner']
    #objs = db['objs']
    # temp for demonstration
    dogClass = { "_id" : 'ObjectId("5617b2fb5632c6d04dc9edca")', "name" : "dog", "tag" : "NN", "class" : True }
    dog = { "_id" : 'ObjectId("5617b3305632c6d04dc9edcb")', "name" : "dog", "type" : 'ObjectId("5617b2fb5632c6d04dc9edca")', "attr":[], "tag":"NN"}
    # John is old. John is a person.
    personClass = {"_id":"9", "name":"person", "tag":"NN", "class":True}
    person = { "_id" : '8', "name" : "person",  "tag":"NN", "type":"9"}
    johnClass = { "_id" : '7', "name" : "John", "tag":"NNP", "class":True, "type":"8"}
    john = { "_id" : 'ObjectId("3")', "name" : "John", "attr":['ObjectId("2")'], "tag":"NNP", "type":"7"}
    # The tree is yellow, old and brown. Yellow is a color. Brown is a color.
    colorClass = {"_id":"0", "name":"colour", "class":True, "tag":"NN"}
    color = {"_id":"1", "name":"colour", "tag":"NN", "type":"0"} # NN appropriate??? TODO
    yellowClass = { "_id" : '2', "name" : "yellow", "tag" : "JJ" , "type" : "1", "class":True}
    yellow = { "_id" : 'ObjectId("5617b3565632c6d04dc9edcc")', "name" : "yellow", "tag" : "JJ" , "type" : "2"}
    brown = { "_id" : 'ObjectId("1")', "name" : "brown", "tag" : "JJ", "type":"3" }
    brownClass = { "_id" : '3', "name" : "brown", "tag" : "JJ", "type":"1", "class":True }
    old = { "_id" : 'ObjectId("2")', "name" : "old", "tag" : "JJ" }
    treeClass = { "_id" : 'ObjectId("5617b3715632c6d04dc9edcd")', "name" : "tree", "tag" : "NN", "class" : True }
    tree = { "_id" : 'ObjectId("5618bc70c937ac93946f9325")', "name" : "tree", "tag" : "NN",
      "type" : 'ObjectId("5617b3715632c6d04dc9edcd")', "attr" : [  'ObjectId("5617b3565632c6d04dc9edcc")' , 'ObjectId("1")' , 'ObjectId("2")'] }

    #barkClass = {"_id":'ObjectId("56asa23131231asd2231")', "name":"bark", "class":True}
    #bark = { "_id" : 'ObjectId("5618c2e3c937ac93946f9326")', "name" : "bark", "tag" : "VBD",
    #  "actors" : [  {  "_id" : 'ObjectId("5617b3305632c6d04dc9edcb")' } ], "prep":{"at":['ObjectId("5618bc70c937ac93946f9325")']} }

    age = { "_id" : '5', "name" : "age", "tag" : "JJ", "type":"6"}
    ageClass = { "_id" : '6', "name" : "age", "tag" : "JJ", "class":True }

    entities = []
    temp_entities = [dog, dogClass, tree, treeClass, yellow, yellowClass, brown, brownClass,
                old, age, ageClass, john, johnClass, person, personClass, color, colorClass]

    st1_entities = [

    ]
    next_id = 1

    def insert_attrs(raw_attrs):
        for raw in raw_attrs:
            raw[KEY_ID] = DbHelper.next_id
            DbHelper.next_id+=1
            DbHelper.entities.append(raw)
        return list(map(get_id, raw_attrs))


    def insert_actor_or_actee(entity):
        existing_entities = get_entities_with(KEY_NAME, entity["name"])
        if len(existing_entities)==0:
            entity[KEY_ID] = DbHelper.next_id
            DbHelper.next_id+=1
            entity[KEY_ATTR] = DbHelper.insert_attrs(entity[KEY_ATTR])
            DbHelper.entities.append(entity)
            return entity
        else:
            existing_attrs= existing_entities[0][KEY_ATTR]
            new_attrs = set()
            for attr in entity[KEY_ATTR]:
                if attr[KEY_NAME] not in list(map(lambda  x: get_name(DbHelper.resolve(x)), existing_attrs)):
                    new_attrs.add(attr)
            existing_attrs.extend(new_attrs)
            return existing_entities[0]


    def insert_action(entity):
        entity[KEY_ID] = DbHelper.next_id
        DbHelper.next_id+=1
        entity[KEY_ATTR] = DbHelper.insert_attrs(entity[KEY_ATTR])
        DbHelper.entities.append(entity)
        return entity


    def merge_entity(entity):
        pass # TODO:

    def __init__(self):
        pass #any setup if required such as establishing data connection to db, allow creation of multiple for
    # representing multiple data banks

    def resolve(_id):
        # TODO: Ensure retrieved data is normalised, such as:
        # 1. Filling in non-existent attr or type values with defaults (may not be necessary with the get_<key> functions

        # implement a cache to prevent creation of multiple references
        try:
            return next(i for i in DbHelper.entities if get_id(i)==_id)
        except StopIteration:
            raise Exception("DbHelper: Could not find " + str(_id) + " in database!")

def _get_entities_in(entity, key):
    '''
    :param entity: entity with some list of objectIds which are to be dereferenced
    :param key: entity[key] is used to access the list of objectIds to dereference
    :return: list of dereferenced entities
    '''
    dereferenced_entities = []
    for i in entity[key]:
        dereferenced_entities.append(DbHelper.resolve(i))

    return dereferenced_entities


def get_entities_with(key, value):
    return [i for i in DbHelper.entities if i[key]==value and not is_class(i)]


def get_class(entity):
    type = get_type(entity)
    return DbHelper.resolve(type) if not type is None else None


# these get_<key> type functions are meant to be used instead of direct dictionary access in case we decide to accomodate
# some sortf of inheritance etc. Or should it be done by resolve? Either way no harm.

def get_id(entity):
    return entity[KEY_ID]


def get_name(entity):
    return entity[KEY_NAME]


def get_tag(entity):
    return entity[KEY_TAG]


def get_type(entity):
    return None if KEY_TYPE not in entity else entity[KEY_TYPE]


def is_class(entity):
    return KEY_CLASS in entity and entity[KEY_CLASS] == True # defensive


def get_resolved_type(entity):
    return None if KEY_TYPE not in entity else DbHelper.resolve(entity[KEY_TYPE])


def get_super_type(entity):
    '''
    A super type is not just an object's type (class), it is the class of its class. The super type of a yellow object
    is the type of the type i.e the type(type(yellow)) i.e type(yellow class)
    :param entity:
    :return:
    '''
    ctr = 0
    while not entity is None:
        if is_class(entity):
            if ctr == 1: return entity
            ctr+=1
        entity = get_resolved_type(entity)
    return None


def get_attrs(entity):
    return [] if KEY_ATTR not in entity else _get_entities_in(entity, KEY_ATTR)
