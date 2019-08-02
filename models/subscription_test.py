import unittest

from .subscription import Subscription
from .plan import Plan

from .model_test import ModelTestCase

class TestSubscription(ModelTestCase):
    def test_eq(self):
        s1 = Subscription('1/1/2019', Plan('p1', 15.3, 3))
        s2 = Subscription('1/2/2019', Plan('p1', 15.3, 3))
        s3 = Subscription('1/1/2019', Plan('p1', 15.3, 3))
        s4 = Subscription('1/1/2019', Plan('p1', 15.4, 3))

        self.assertEqual(s1, s1)
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(s1, s4)
        self.assertNotEqual(s1, s3)

if __name__ == '__main__':
    unittest.main()