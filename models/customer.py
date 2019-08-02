
from models import Model, autoproperty, baseproperties

@baseproperties
@autoproperty(name='')
@autoproperty(password='')
@autoproperty(email='')
@autoproperty(subscription=None)
class Customer(Model):
    def __init__(self, name, password, email, subscription):
        '''
        Creates a new Costumer object
            :param name: str
            :param password: str
            :param email: str
            :param subscription: Subscription
        '''
        super().__init__()
        self.name = name
        self.password = password
        self.email = email
        self.subscription = subscription

    def __eq__(self, other):
        return super().__eq__(other) and \
            self.name == other.name and \
            self.password == other.password and \
            self.email == other.email and \
            self.subscription == other.subscription