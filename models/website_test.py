import unittest

from .validator.validator import ValidatorException
from .website import Website
from .customer import Customer

from .model_test import ModelTestCase

class TestPlan(ModelTestCase):
    def test_eq(self):
        c1 = Customer('c1', '123456', 'abc@example.com', None)
        w1 = Website('h1', c1)

        w2 = Website('h2', None)

        w3 = Website('h1', None)

        self.assertEqual(w1, w1)
        self.assertNotEqual(w1, w2)
        self.assertNotEqual(w1, w3)

    def test_invalid_url(self):
        with self.assertRaises(ValidatorException):
            Website(None, None)

if __name__ == '__main__':
    unittest.main()