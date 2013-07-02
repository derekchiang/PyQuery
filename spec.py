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


class Attribute(object):

    """ Specify a condition on an attribute of an object or dict

    Examples:
    Attribute('is_public', IsTrue())
        - would match public images
    Attribute('created_at', GreaterThan(yesterday))
        - would match objects created more recently than yesterday
    """

    def __init__(self, attr, value_spec):
        self.attr = attr
        self.value_spec = value_spec

    def match(self, obj):
        value = getattr(obj, self.attr, None)
        if value is None:
            value = obj.get(self.attr)
        return self.value_spec.match(value)


class Not(object):

    """ Negate a specification. """

    def __init__(self, spec):
        self.spec = spec

    def match(self, obj):
        return not self.spec.match(obj)


class And(object):

    """ Returns true if all given specifications are true. """

    def __init__(self, *specs):
        self.specs = specs

    def match(self, obj):
        for spec in self.specs:
            if not spec.match(obj):
                return False
        return True


class Or(object):

    """ Returns true if any given specification is true. """

    def __init__(self, *specs):
        self.specs = specs

    def match(self, obj):
        for spec in self.specs:
            if spec.match(obj):
                return True
        return False


class GT(object):

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value > self.value


class GTE(object):

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value >= self.value


class LT(object):

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value < self.value


class LTE(object):

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value <= self.value


class EQ(object):

    def __init__(self, value):
        self.value = value

    def match(self, value):
        return value == self.value


class IsTrue(object):

    def match(self, value):
        return value is True


class IsNone(object):

    def match(self, value):
        return value is None
