import unittest

from .subscription import Subscription
from .plan import Plan
from .customer import Customer

class TestCustomer(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()