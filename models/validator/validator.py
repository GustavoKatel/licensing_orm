
class ValidatorException(Exception):
    def __init__(self, value, *args, **kwargs):
        super().__init__('Invalid value: "{}"'.format(value), *args, kwargs)

class Validator(object):
    '''
    Base validator. Inherit from this class to add validations to Model properties
    '''
    def validate(self, value):
        pass