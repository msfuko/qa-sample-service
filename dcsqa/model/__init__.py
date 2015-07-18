"""
The class is the super class of all models, which will check the props map in subclass.
Using for validate whether the data type of props is expected
"""
import json
from flask import current_app


class BaseObject(object):

    def __init__(self, **kwargs):
        # Cache the keys for validity checks
        self.__dict__['propnames'] = self.props.keys()

        # result properties fields
        self.__dict__['properties'] = {}

        # set attributes
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __setattr__(self, name, value):
        # not checking item, set attribute
        if name not in self.propnames:
            return dict.__setattr__(self, name, value)

        else:
            # check if the type matches expected_type, if no, bypass
            expected_type = self.props[name][0]

            if isinstance(value, expected_type):
                return self.properties.__setitem__(name, value)
            else:
                current_app.logger.warn("Field {name} is required in type {expected_type} but {current_type}, Skip".
                                        format(name=name, expected_type=expected_type, current_type=type(value)))

    def get_json(self, indent=4, sort_keys=True, separators=(',', ': ')):
        # check if the required fields are all in
        for name, (default_type, required) in self.props.items():
            if required and name not in self.properties:
                rtype = getattr(self, 'resource_type', str(default_type))
                raise ValueError("Properties {name} is required in type {rtype}".
                                 format(name=name, rtype=rtype))

        current_app.logger.debug(json.dumps(self.properties, indent=indent, sort_keys=sort_keys, separators=separators))
        return self.properties

