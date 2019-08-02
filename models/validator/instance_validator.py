import re

from .validator import Validator
from .not_none_validator import NotNoneValidator

class InstanceValidator(NotNoneValidator):
    def __init__(self, klass):
        super().__init__()
        self.klass = klass

    def validate(self, value):
        return super().validate(value) and \
            isinstance(value, self.klass)