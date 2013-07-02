class Model(object):
    is_standalone = True
    relations = []

    def __init__(self, object):
        pass

    @classmethod
    def add_relation(cls, relation):
        cls.relations.push(relation)