from models import Model, autoproperty, baseproperties

@baseproperties
@autoproperty(url='')
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