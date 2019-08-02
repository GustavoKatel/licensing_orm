from datetime import datetime

from models import Model, autoproperty, baseproperties
from models.validator.instance_validator import InstanceValidator

@baseproperties
@autoproperty(renewal_date=None, validators=[InstanceValidator(datetime)])
@autoproperty(plan=None)
class Subscription(Model):
    def __init__(self, renewal_date, plan):
        '''
        Creates a new Subscription object
            :param renewal_date: datetime point in the future
            :param plan: Plan
        '''
        super().__init__()
        self.renewal_date = renewal_date
        self.plan = plan

    def __eq__(self, other):
        return super().__eq__(other) and \
            self.renewal_date == other.renewal_date and \
            self.plan == other.plan