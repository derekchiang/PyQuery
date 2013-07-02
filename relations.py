class Relation(object):
    def __init__(self, modelA, modelB):
        self.modelA = modelA
        self.modelB = modelB

    def first(self, model, specs):
        self.fetch(specs, 1)

    def fetch(self, model, specs, number):
        self.all(specs)[:number]

    def all(self, model, specs):
        pass

    def delete(self, model, specs):
        pass

    def insert(self, model, specs, values):
        pass

class OneToOne(Relation):
    pass

class OneToMany(Relation):
    pass

class ManyToOne(Relation):
    pass

class ManyToMany(Relation):
    pass

def add_relation(relation):
    relation.modelA.add_relation(relation)
    relation.modelB.add_relation(relation)