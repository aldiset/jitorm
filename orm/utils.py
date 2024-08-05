from numba import jit

@jit(nopython=True)
def map_to_instance(cls, data):
    instance = cls()
    for key, value in data.items():
        setattr(instance, key, value)
    return instance

def instance_to_dict(instance):
    return {field: getattr(instance, field) for field in instance._fields}
