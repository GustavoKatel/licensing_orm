from .autoproperty import autoproperty

def baseproperties(cls):
    '''
    creates base properties for models
    base properties includes:
    - id: int (autoincrement)
    - created_at
    - updated_at
    '''
    cls = autoproperty(id=0, hasSet=False)(cls)
    cls = autoproperty(created_at='')(cls)
    cls = autoproperty(updated_at='')(cls)
    return cls