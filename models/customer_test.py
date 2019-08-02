import unittest

from .subscription import Subscription
from .plan import Plan
from .customer import Customer
from .seeds.seeds import SEEDS

from .model_test import ModelTestCase

class TestCustomer(ModelTestCase):
    def test_eq(self):
        s1 = Subscription('1/1/2019', Plan('p1', 15.3, 3))
        s2 = Subscription('1/1/2019', Plan('p1', 25.3, 4))

        c1 = Customer('c1', '123456', 'abc@example.com', s1)
        c2 = Customer('c2', '123456', 'abc@example.com', s1)
        c3 = Customer('c1', '123456', 'abc@example.com', s1)
        c4 = Customer('c1', '123456', 'abc@example.com', s2)

        self.assertEqual(c1, c1)
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c4)
        self.assertNotEqual(c1, c3)

    def test_has_subscription(self):
        c1 = Customer('c1', '123456', 'abc@example.com', None)
        self.assertFalse(c1.has_subscription())

        s1 = Subscription('1/1/2019', Plan('p1', 15.3, 3))
        c1 = Customer('c1', '123456', 'abc@example.com', s1)
        self.assertTrue(c1.has_subscription())

    def test_subscribe_from_empty(self):
        Plan.seed(SEEDS['plans'])

        c1 = Customer('c1', '123456', 'abc@example.com', None)
        self.assertFalse(c1.has_subscription())

        c1.subscribe('single')
        self.assertTrue(c1.has_subscription())

    def test_subscribe_change_plans(self):
        Plan.seed(SEEDS['plans'])

        s1 = Subscription('1/1/2019', Plan('p1', 15.3, 3))
        c1 = Customer('c1', '123456', 'abc@example.com', s1)
        self.assertTrue(c1.has_subscription())
        self.assertEqual(c1.subscription.plan.name, 'p1')

        c1.subscribe('single')
        self.assertTrue(c1.has_subscription())
        self.assertEqual(c1.subscription.plan.name, 'single')

    def test_subscribe_invalid_plan(self):
        # do not seed, so we can raise an exception
        # Plan.seed(SEEDS['plans'])

        c1 = Customer('c1', '123456', 'abc@example.com', None)
        self.assertFalse(c1.has_subscription())

        with self.assertRaisesRegex(Exception, 'Invalid plan'):
            c1.subscribe('single')

        self.assertFalse(c1.has_subscription())

if __name__ == '__main__':
    unittest.main()