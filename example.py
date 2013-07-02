from model import Model
from relations import OneToMany, add_relation
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, relationship, backref

from pycassa.types import IntegerType, BytesType, deserialize
import pycassa

from query import Query
from spec import EqualTo

# An actual Nova API, implemented using the generic framework
def compute_node_get(context, compute_id):
    result = Query(ComputeNode).filter(EqualTo('id', compute_id)).first()
    return result

# Generic declaration

class Model(object):
    is_standalone = True
    relations = []

class Service(Model):
    pass

class ComputeNode(Model):
    pass

class ServiceHasManyComputeNode(OneToMany):
    def query(attributes):
        pass

# This method adds the relationship to both class' `relations` field
add_relation(ServiceHasManyComputeNode(Service, ComputeNode))

# Generic definition of Query
class GenericQuery(object):
    def __init__(self, model):
        self.model = model
        # some other stuff...

    # some other methods...

    def first(self):
        if self.model.is_standalone:
            self.get(self.attribute, 1)
        else:
            for rel in self.model.relations:
                result = rel.query(self.attribute)
                if result is not None:
                    return result

    # this method should be implemented by the driver
    def get(attribute, number):
        pass

# SQLAlchemy

class Service(Model, sqlalchemy.Model):
    id = Column(Integer, primary_key=True)

class ComputeNode(Model, sqlalchemy.Model):
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    service = relationship(Service,
                           backref=backref('compute_node'),
                           foreign_keys=service_id,
                           primaryjoin='and_('
                                'ComputeNode.service_id == Service.id,'
                                'ComputeNode.deleted == 0)')

class Query(GenericQuery):
    def get(attribute, number):
        if isinstance(attribute, EqualTo):
            # I know this is not valid python code, but you get the idea
            results = sqlalchemy.query(self.model).filter(EqualTo.attr=EqualTo.value).all()
            return results[:number]

# Cassandra

class Service(Model):
    id = IntegerType()
    # Suppose Service stores ComputeNodes as serialized JSON data
    compute_nodes = BytesType()

class ComputeNode(Model):
    is_standalone = False

class ServiceHasManyComputeNode(OneToMany):
    def query(attribute):
        data = pycassa.query(Service).get_all('compute_nodes')
        compute_nodes = deserialize(data)
        for cn in compute_nodes:
            if attribute.match(cn):
                yield cn

        return None

add_relation(ServiceHasManyComputeNode(Service, ComputeNode))