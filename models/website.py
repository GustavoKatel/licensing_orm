from models import Model, autoproperty, baseproperties
from models.validator.instance_validator import InstanceValidator

@baseproperties
@autoproperty(url='', validators=[InstanceValidator(str)])
@autoproperty(customer=None)
class Website(Model):
    def __init__(self, url, customer):
        '''
        Cretes a website object
            :param url: str
            :param customer: Customer
        '''
        super().__init__()
        self.url = url
        self.customer = customer

    def __eq__(self, other):
        return super().__eq__(other) and \
            self.url == other.url and \
            self.customer == other.customer