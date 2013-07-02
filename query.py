#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class QueryImplementation(object):

    """
    Drivers need to implement a class with this interface.
    """

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


class Query(object):

    def __init__(self, query_impl):
        self.specs = []
        self.impl = query_impl
        self.model = None

    def __call__(self, model):
        self.model = model

    def call_impl(func):
        def wrapper(self, *args):
            if self.model.is_standalone:
                return self.impl[func.__name__](*args, **{'model': self.model, 'specs': self.specs})
            else:
                for rel in self.model.relations:
                    result = rel[func.__name__](
                        *args, **{'model': self.model, 'specs': self.specs})
                    if result is not None:
                        return result

                return None

    def filter(self, specification):
        self.specs.push(specification)
        return self

    @call_impl
    def first(self):
        pass

    @call_impl
    def fetch(self, number):
        pass

    @call_impl
    def all(self):
        pass

    @call_impl
    def delete(self):
        pass

    @call_impl
    def insert(self, values):
        pass
