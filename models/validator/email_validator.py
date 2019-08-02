import re

from .validator import Validator

class EmailValidator(Validator):
    email_regex = re.compile(r'[a-z0-9\.\-\_\+]+@[a-z0-9\.\-\_]', re.IGNORECASE)

    def validate(self, value):
        return self.email_regex.match(value) is not None