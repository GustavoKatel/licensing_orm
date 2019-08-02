import unittest
from datetime import datetime

from .subscription import Subscription
from .plan import Plan
from .website import Website
from .customer import Customer
from .seeds.seeds import SEEDS
from .validator.validator import ValidatorException

from .model_test import ModelTestCase

class TestCustomer(ModelTestCase):
    def test_invalid_name(self):
        with self.assertRaises(ValidatorException):
            Customer(None, '123', 'asd@example.com', None)

    def test_invalid_password(self):
        with self.assertRaises(ValidatorException):
            Customer('asd', None, 'asd@example.com', None)

    def test_hashed_password(self):
        c1 = Customer('asd', 'abc', 'asd@example.com', None)
        self.assertNotEqual(c1.password, 'abc')
        self.assertEqual(c1.password, Customer.hash_password('abc'))
        self.assertIsInstance(c1.password, str)

    def test_invalid_email(self):
        with self.assertRaises(ValidatorException):
            Customer('c1', '123', 'asd', None)

        with self.assertRaises(ValidatorException):
            Customer('c1', '123', None, None)

        c1 = Customer('c1', '123', 'asd@example.com', None)
        with self.assertRaises(ValidatorException):
            c1.email = 'asd'

    def test_eq(self):
        s1 = Subscription(datetime.now(), Plan('p1', 15.3, 3))
        s2 = Subscription(datetime.now(), Plan('p1', 25.3, 4))

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

        s1 = Subscription(datetime.now(), Plan('p1', 15.3, 3))
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

        s1 = Subscription(datetime.now(), Plan('p1', 15.3, 3))
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

    def test_subscribe_renewal_date(self):
        Plan.seed(SEEDS['plans'])

        c1 = Customer('c1', '123456', 'abc@example.com', None)
        c1.subscribe('single')
        self.assertTrue(c1.has_subscription())
        self.assertEqual(c1.subscription.plan.name, 'single')

        self.assertEqual(c1.subscription.renewal_date.year, datetime.now().year+1)

    def test_website_create_no_plan(self):
        c1 = Customer('c1', '12345', 'abc@example.com', None)
        with self.assertRaisesRegex(Exception, 'Please subscribe .*'):
            c1.create_website('http://localhost')

    def test_website_create_ok(self):
        Plan.seed(SEEDS['plans'])
        p1 = Plan.find_one({'name': 'single'})

        c1 = Customer('c1', '12345', 'abc@example.com', Subscription(datetime.now(), p1))
        website = c1.create_website('http://localhost')
        self.assertEqual(website.url, 'http://localhost')

    def test_website_create_max_reached(self):
        Plan.seed(SEEDS['plans'])
        p1 = Plan.find_one({'name': 'single'})

        c1 = Customer('c1', '12345', 'abc@example.com', Subscription(datetime.now(), p1))
        c1.create_website('http://localhost')

        with self.assertRaisesRegex(Exception, 'Max websites reached for this plan.*'):
            c1.create_website('http://localhost')

    def test_website_create_max_reached_ok_after_remove(self):
        Plan.seed(SEEDS['plans'])
        p1 = Plan.find_one({'name': 'single'})

        c1 = Customer('c1', '12345', 'abc@example.com', Subscription(datetime.now(), p1))
        c1.create_website('http://localhost')

        with self.assertRaisesRegex(Exception, 'Max websites reached for this plan.*'):
            c1.create_website('http://localhost')

        website = Website.find_one({'customer': c1})
        website.remove()

        c1.create_website('http://localhost:9090')

    def test_website_create_plus_plan(self):
        Plan.seed(SEEDS['plans'])
        p1 = Plan.find_one({'name': 'plus'})

        c1 = Customer('c1', '12345', 'abc@example.com', Subscription(datetime.now(), p1))

        for i in range(3):
            c1.create_website('http://localhost')
            total = Website.count({'customer': c1})
            self.assertEqual(total, i+1)

        with self.assertRaisesRegex(Exception, 'Max websites reached for this plan.*'):
            c1.create_website('http://localhost')

    def test_website_create_infinite_plan(self):
        Plan.seed(SEEDS['plans'])
        p1 = Plan.find_one({'name': 'infinite'})

        c1 = Customer('c1', '12345', 'abc@example.com', Subscription(datetime.now(), p1))

        for i in range(100):
            c1.create_website('http://localhost')
            total = Website.count({'customer': c1})
            self.assertEqual(total, i+1)

if __name__ == '__main__':
    unittest.main()