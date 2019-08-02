import re

from .validator import Validator

class NotNoneValidator(Validator):
    def validate(self, value):
        return value is not None