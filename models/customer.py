from datetime import datetime, timedelta

from models import Model, autoproperty, baseproperties

from models.plan import Plan
from models.subscription import Subscription

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

    def has_subscription(self):
        '''
        returns true if the user has a subscription, false otherwise
        :rtype: boolean
        '''
        return self.subscription is not None

    def subscribe(self, plan_name):
        '''
        subscribe the user to a plan
        :param plan_name: str name of the plan
        '''
        plan = Plan.find_one({'name': plan_name})
        if plan is None:
            raise Exception('Invalid plan')

        if not self.has_subscription():
            self.subscription = Subscription.create('today', plan)
        else:
            self.subscription.plan = plan

        # about 365 days, 5 hours, 48 minutes, and 46 seconds
        renewal_date = datetime.now() + timedelta(days=365.2422)
        self.subscription.renewal_date = renewal_date
