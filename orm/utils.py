def map_to_instance(cls, data):
    if not isinstance(data, tuple):
        raise TypeError(f"Expected a tuple, got {type(data).__name__}")
    fields = list(cls._fields.keys())
    if len(data) != len(fields):
        raise ValueError("Data length does not match the number of fields")
    instance = cls(**dict(zip(fields, data)))
    return instance

def instance_to_dict(instance):
    return {field: getattr(instance, field) for field in instance._fields if field!="id"}
