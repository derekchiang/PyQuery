from query import QueryImplementation
from relations import OneToOne, OneToMany, ManyToOne, ManyToMany
from spec import *
from model import Model

from sqlalchemy.orm import sessionmaker

engine = None  # Need to be set up
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class SQLAlchemyQueryImpl(QueryImplementation):

    def first(self, model, specs):
        self.fetch(model, specs, 1)

    def fetch(self, model, specs, number):
        return self.all(model, specs)[:number]

    def all(self, model, specs):
        query = session.query(model)

        for spec in specs:
            if isinstance(spec.value_spec, EQ):
                query = query.filter(model[spec.attr] == spec.value_spec.value)
            elif isinstance(spec.value_spec, GT):
                query = query.filter(model[spec.attr] > spec.value_spec.value)
            elif isinstance(spec.value_spec, LT):
                query = query.filter(model[spec.attr] < spec.value_spec.value)
            elif isinstance(spec.value_spec, GTE):
                query = query.filter(model[spec.attr] >= spec.value_spec.value)
            elif isinstance(spec.value_spec, LTE):
                query = query.filter(model[spec.attr] <= spec.value_spec.value)

        return query.all()

    def delete(self, model, specs):
        instances = self.all(model, specs)
        for i in instances:
            session.delete(i)

        session.commit()

    def insert(self, model, specs, values):
        if specs:
            instances = self.all(model, specs)
            for i in instances:
                for k, v in values:
                    i[k] = v
                session.add(i)
        else:
            # if specs is empty, then we insert a new instance
            # rather than replace old ones
            new_instance = model()
            for k, v in values:
                new_instance[k] = v
            session.add(i)

        session.commit()
