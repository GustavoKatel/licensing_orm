from models import Model, autoproperty, baseproperties

@baseproperties
@autoproperty(name='')
@autoproperty(price=0.0)
@autoproperty(number_websites=0)
class Plan(Model):
    def __init__(self, name, price, number_websites):
        '''
        Creates a new Plan object
            :param name: str
            :param price: float
            :param number_websites: int
        '''
        super().__init__()
        self.name = name
        self.price = price
        self.number_websites = number_websites


    def __eq__(self, other):
        return super().__eq__(other) and \
            self.name == other.name and \
            self.price == other.price and \
            self.number_websites == other.number_websites