from query import QueryImplementation
from relations import OneToOne, OneToMany, ManyToOne, ManyToMany
from spec import *
from model import Model

from pycassa.columnfamilymap import ColumnFamilyMap
# from pycassa.index import create_index_expression, create_index_clause
import pycassa.index as index
from pycassa.index import create_index_clause, create_index_expression

pool = None  # Need to be set up


class CassandraQueryImpl(QueryImplementation):

    def first(self, model, specs):
        self.fetch(specs, 1)

    def fetch(self, model, specs, number):
        expressions = []

        for spec in specs:
            if isinstance(spec.value_spec, EQ):
                expressions.push(
                    create_index_expression(spec.attr, spec.value_spec.value))
            elif isinstance(spec.value_spec, GT):
                expressions.push(create_index_expression(
                    spec.attr, spec.value_spec.value, index.GT))
            elif isinstance(spec.value_spec, LT):
                expressions.push(create_index_expression(
                    spec.attr, spec.value_spec.value, index.LT))
            elif isinstance(spec.value_spec, GTE):
                expressions.push(create_index_expression(
                    spec.attr, spec.value_spec.value, index.GTE))
            elif isinstance(spec.value_spec, LTE):
                expressions.push(create_index_expression(
                    spec.attr, spec.value_spec.value, index.LTE))

        cfm = ColumnFamilyMap(model, pool, model.cf_name)
        clause = create_index_clause([state_expr, bday_expr], count=number)

        def value_only(lst):
            values = []
            for key, value in lst:
                values.push(value)
            return values

        return value_only(cfm.get_indexed_slices(clause))

    def all(self, model, specs):
        if specs:
            # Obviously this isn't the most elegant way to get all objects
            return self.fetch(model, specs, number=9999999999)
        else:
            # If there is no specification, get everything
            cfm = ColumnFamilyMap(model, pool, model.cf_name)
            return cfm.get_range()

    def delete(self, model, specs):
        instances = self.all(model, specs)
        cfm = ColumnFamilyMap(model, pool, model.cf_name)
        for i in instances:
            cfm.remove(i)

    def insert(self, model, specs, values):
        if specs:
            instances = self.all(model, specs)
            cfm = ColumnFamilyMap(model, pool, model.cf_name)
            for i in instances:
                for k, v in values:
                    i[k] = v
                cfm.insert(i)
        else:
            # if specs is empty, then we insert a new instance
            # rather than replace old ones
            new_instance = model()
            for k, v in values:
                new_instance[k] = v
            cfm.insert(i)
