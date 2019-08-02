import unittest

from .model import Model
from .autoproperty import autoproperty
from .baseproperties import baseproperties

@baseproperties
@autoproperty(name='')
class ModelTest(Model):
    def __init__(self, name):
        super().__init__()
        self.name = name

@baseproperties
@autoproperty(price=0.0)
class ModelTest2(Model):
    def __init__(self, price):
        super().__init__()
        self.price = price

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        Model.reset_all_containers()

class TestModel(ModelTestCase):
    def test_property(self):
        model = ModelTest('test')
        self.assertEqual(model.name, 'test')
        #pylint: disable=no-member
        self.assertEqual(model._name, 'test')

        model.name = 'test2'
        self.assertEqual(model.name, 'test2')
        #pylint: disable=no-member
        self.assertEqual(model._name, 'test2')

        properties = model.__properties__
        self.assertEqual(['updated_at', 'created_at', 'id', 'name'], properties)

    def test_property_cannot_set_id(self):
        model = ModelTest('test')
        with self.assertRaises(Exception):
            model.id = 123

    def test_property_updated_at(self):
        model = ModelTest('test')
        model.name = 'test2'
        self.assertIsNotNone(model.updated_at)

    def test_property_created_at(self):
        model = ModelTest('test')
        model.name = 'test2'
        model.save()

        self.assertIsNotNone(model.created_at)
        # we have updated
        self.assertNotEqual(model.created_at, model.updated_at)

        ret = ModelTest.find_one({'name': 'test2'})
        self.assertEqual(ret.created_at, model.created_at)
        self.assertEqual(ret.updated_at, model.updated_at)

    def test_container(self):
        self.assertEqual(ModelTest.all(), [])

        m1 = ModelTest.create('abc')
        self.assertEqual(len(ModelTest.all()), 1)
        self.assertEqual(ModelTest.all()[0].name, m1.name)

        m2 = ModelTest2.create(15.3)
        self.assertEqual(len(ModelTest2.all()), 1)
        self.assertEqual(ModelTest2.all()[0].price, m2.price)

    def test_find(self):
        m1 = ModelTest.create('abc')
        m2 = ModelTest.create('abc 2')
        m3 = ModelTest.create('abc')

        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 2)

        self.assertEqual(ret[0], m1)
        self.assertNotEqual(ret[1], m1)

        self.assertEqual(ret[1], m3)
        self.assertNotEqual(ret[0], m3)

        ret = ModelTest.find({'name': 'abc 2'})
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0], m2)

    def test_count(self):
        ModelTest.create('abc')
        ModelTest.create('abc 2')
        ModelTest.create('abc')

        ret = ModelTest.count({'name': 'abc'})
        self.assertEqual(ret, 2)

        ret = ModelTest.count({'name': 'abc 2'})
        self.assertEqual(ret, 1)

    def test_find_one(self):
        m1 = ModelTest.create('abc')
        ModelTest.create('abc 2')
        ModelTest.create('abc')

        ret = ModelTest.find_one({'name': 'abc'})
        self.assertEqual(ret, m1)

    def test_eq(self):
        m1 = ModelTest('abc')
        m2 = ModelTest2(15.4)
        self.assertNotEqual(m1, m2)

    def test_save(self):
        m1 = ModelTest('abc')
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 0)

        m1.save()
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 1)

    def test_update(self):
        m1 = ModelTest('abc')
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 0)

        m1.save()
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 1)

        m1.name = 'test'
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 1)

        m1.save()
        ret = ModelTest.find({'name': 'abc'})
        self.assertEqual(len(ret), 0)

        ret = ModelTest.find({'name': 'test'})
        self.assertEqual(len(ret), 1)

    def test_seed(self):
        seed_data = [
            ['test1'],
            {'name': 'test2'}
        ]

        results = ModelTest.seed(seed_data)
        self.assertEqual(2, len(results))
        self.assertEqual('test1', results[0].name)
        self.assertEqual('test2', results[1].name)

    def test_remove(self):
        m1 = ModelTest.create('abc')
        ModelTest.create('abc 2')
        m3 = ModelTest.create('abc')

        ret = ModelTest.count()
        self.assertEqual(ret, 3)

        m1.remove()
        ret = ModelTest.count()
        self.assertEqual(ret, 2)
        self.assertEqual(ModelTest.find_one({'name': 'abc'}), m3)

        ModelTest.remove_object(m3)
        ret = ModelTest.count()
        self.assertEqual(ret, 1)
        self.assertIsNone(ModelTest.find_one({'name': 'abc'}))

if __name__ == '__main__':
    unittest.main()