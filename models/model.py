from copy import deepcopy
from datetime import datetime

from .autoproperty import autoproperty

_global_containers = {}

class Model(object):
    """
    Base model class to be shared in all models
    """
    def __init__(self, created_at=None, updated_at=None, id=None):
        if id is None:
            id = self.__class__.next_sequence()
        self._id = id

        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at

        if updated_at is None:
            updated_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        '''
        default __repr__ for all models
        '''
        s = '['
        s += ' '.join(
            map(
                lambda prop: '{}={}'.format(prop, getattr(self, prop, None)),
                getattr(self, '__properties__', [])
            )
        )
        return s + ']'

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
            self._id == other._id

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if attr in ['created_at', 'updated_at', '_created_at', '_updated_at']:
            return
        self.updated_at = datetime.now()

    def save(self):
        '''
        saves this instance to the container
        '''
        self.__class__.save_object(self)

    def remove(self):
        '''
        removes this instance from the container
        '''
        self.__class__.remove_object(self)

    @staticmethod
    def _get_global_container(cls):
        '''
        manages all containers from all models
        '''
        return _global_containers.get(cls, [])

    @staticmethod
    def _set_global_container(cls, ct):
        '''
        manages all containers from all models
        '''
        _global_containers[cls] = ct

    @staticmethod
    def reset_all_containers():
        _global_containers.clear()

    @classmethod
    def _get_container(cls):
        '''
        Returns the base storage for this class
        '''
        return cls._get_global_container(cls)

    @classmethod
    def _set_container(cls, ct):
        '''
        Updates the base storage for this class
        '''
        cls._set_global_container(cls, ct)

    @classmethod
    def next_sequence(cls):
        n = getattr(cls, '_next_sequence', 1)
        setattr(cls, '_next_sequence', n+1)
        return n

    @classmethod
    def clear(cls):
        '''
        Clear all stored items
        '''
        cls._set_container([])

    @classmethod
    def all(cls):
        '''
        all returns all the stored items for this model
        '''
        ct = cls._get_container()
        return deepcopy(ct)

    @classmethod
    def create(cls, *args, **kwargs):
        '''
        creates a new model and stores it
        '''
        obj = cls(*args, **kwargs)
        ct = cls._get_container()
        ct.append(obj)
        cls._set_container(ct)

        return deepcopy(obj)

    @classmethod
    def find(cls, query=None):
        '''
        queries stored items for this model
        :param query: dict where keys are properties
        '''
        if query == None:
            query = {}

        ct = cls._get_container()
        results = []
        for item in ct:
            valid = True
            for key, value in query.items():
                if not getattr(item, key, None) == value:
                    valid = False

            if valid:
                results.append(deepcopy(item))

        return results

    @classmethod
    def count(cls, query=None):
        '''
        returns the number of items matching the query
        :param query: dict where keys are properties
        :rtype int:
        '''
        if query == None:
            query = {}

        ct = cls._get_container()
        results = 0
        for item in ct:
            valid = True
            for key, value in query.items():
                if not getattr(item, key, None) == value:
                    valid = False

            if valid:
                results += 1

        return results

    @classmethod
    def find_one(cls, query):
        '''
        queries stored items for this model. Returns only the first result
        :param query: dict where keys are properties
        '''
        if query == None:
            query = {}

        ct = cls._get_container()
        for item in ct:
            valid = True
            for key, value in query.items():
                if not getattr(item, key, None) == value:
                    valid = False

            if valid:
                return deepcopy(item)

        return None

    @classmethod
    def save_object(cls, obj):
        '''
        saves an object to this container
        :param obj: Model
        '''
        ct = cls._get_container()
        to_replace = -1
        for i, se in enumerate(ct):
            if se.id == obj.id:
                to_replace = i

        if to_replace >= 0:
            ct[to_replace] = deepcopy(obj)
        else:
            ct.append(deepcopy(obj))

        cls._set_container(ct)

    @classmethod
    def _seed_from_list(cls, data):
        obj = cls.create(*data)
        return obj

    @classmethod
    def _seed_from_dict(cls, data):
        obj = cls.create(**data)
        return obj

    @classmethod
    def seed(cls, data):
        '''
        seeds the container with data in `data`
        :param data: list<list|dict>
        '''
        results = []
        for entry in data:
            if isinstance(entry, dict):
                results.append(cls._seed_from_dict(entry))
            elif isinstance(entry, list):
                results.append(cls._seed_from_list(entry))
            else:
                raise Exception('Invalid data type. Required list or dict')

        return results

    @classmethod
    def remove_object(cls, obj):
        '''
        removes an object from this model container
        '''
        ct = cls._get_container()
        ct.remove(obj)
        cls._set_container(ct)