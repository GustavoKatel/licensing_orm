import unittest

from .plan import Plan

from .model_test import ModelTestCase

class TestPlan(ModelTestCase):
    def test_eq(self):
        p1 = Plan('p1', 15.4, 3)
        p2 = Plan('p2', 15.3, 3)
        p3 = Plan('p1', 15.4, 3)

        self.assertEqual(p1, p1)
        self.assertNotEqual(p1, p2)
        self.assertNotEqual(p1, p3)

if __name__ == '__main__':
    unittest.main()