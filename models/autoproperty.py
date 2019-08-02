from .validator import ValidatorException

def autoproperty(**kwargs):
    '''
    Automatically creates properties within a model
    By default properties have a getter, a setter and a deleter. All three can be disabled.
    Eg.:
    @autoproperty(name='')
    class User(object):
        def __init__(self, name):
            self._name = name

    @autoproperty(name='', hasSet=False)
    class User(object):
        def __init__(self, name):
            # Error! Set is disabled
            self.name = name
    '''

    hasGet = True
    hasSet = True
    hasDel = True
    baseName = ''
    innerName = '_{}'
    defaultValue = None
    validators = []

    # gets the first kwarg and assume the rest are args
    baseName, defaultValue = list(kwargs.items())[0]
    innerName = innerName.format(baseName)
    kwargs.pop(baseName)

    for key, value in kwargs.items():
        if key == 'hasGet':
            hasGet = value
        elif key == 'hasSet':
            hasSet = value
        elif key == 'hasDel':
            hasDel = value
        elif key == 'validators':
            validators = value

    def _get(obj):
        return getattr(obj, innerName, defaultValue)

    def _set(obj, v):
        for vdt in validators:
            if not vdt.validate(v):
                raise ValidatorException(v, property=baseName)
        setattr(obj, innerName, v)

    def _del(obj):
        delattr(obj, innerName)

    def decorator(cls):
        prop = property(_get if hasGet else None, _set if hasSet else None,
                        _del if hasDel else None)

        setattr(cls, baseName, prop)

        props = getattr(cls, '__properties__', [])
        props.insert(0, baseName)
        setattr(cls, '__properties__', props)

        return cls

    return decorator
