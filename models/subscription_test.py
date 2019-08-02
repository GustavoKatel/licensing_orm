import unittest
from datetime import datetime, timedelta

from .validator.validator import ValidatorException
from .subscription import Subscription
from .plan import Plan

from .model_test import ModelTestCase

class TestSubscription(ModelTestCase):
    def test_eq(self):
        s1 = Subscription(datetime.now(), Plan('p1', 15.3, 3))
        s2 = Subscription(datetime.now()+timedelta(days=1), Plan('p1', 15.3, 3))
        s3 = Subscription(datetime.now(), Plan('p1', 15.3, 3))
        s4 = Subscription(datetime.now(), Plan('p1', 15.4, 3))

        self.assertEqual(s1, s1)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, s3)

    def test_invalid_renewal_date(self):
        with self.assertRaises(ValidatorException):
            Subscription(None, None)

if __name__ == '__main__':
    unittest.main()