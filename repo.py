class Model(object):
    def insert(self, values):
        pass

    def delete(self):
        pass

    def update(self):
        pass

declare_relations(relations.HAS_MANY, models.Service, models.ComputeNode)

query(models.Service).filter(Attribute('id', EqualTo('123'))).delete()

query(models.ComputeNode).filter(Attribute('service_id', EqualTo('123'))).delete()

query(models.ComputeNode).filter(Attribute('id', EqualTo('123'))).first()

query(ComputeNode, Service, Attribute('id', EqualTo('123')))


I want to get all computenodes that belong to a service

I want to get all computenodes that have this attribute

def deleteHasMany(parent, child, parent_attr, child_attr):
    attr = getattr(parent, parent_attr)
    query(child).filter(Attribute(child_attr, EqualTo(attr))).delete()

def deleteChild(parent, child, child_attr):
    if child is ComputeNode:
        compute_nodes = deserialize(parent.compute_nodes)
        for cn in compute_nodes:
            if not child_attr.match(cn):
                nodes.push(cn)



relationships += HasManyRelationship(models.Service, models.ComputeNode)

filter(belongTo(withAttr(models.Service, 'id', '123')))



class ServiceHasManyComputeNodes(HasManyRelationship):
    def __init__(self, parent, child):


    def queryChildren(attributes):
        query(child).filter(service_id = parent_attr)

if isStandalone(model):
    delete(model)
else:



def query(model):
    if isStandalone(model):
        return Query(model)
    else:
        return RelationalQuery(model).update('')

class Query(object):
    def __init__(model):
        pass

        does the model exist?

            if so, query it directly

            if not, does it belong to anyone?

                if not, return an error plz?

                if so, ask the parent model for it?
    
    def filter(self, specs):
        pass

    def insert(self, values):
        pass

    def delete(self):
        pass

    def update(self, values):
        pass

    def first(self):
        pass

    def all(self):
        pass

class RelationalQuery(object):
