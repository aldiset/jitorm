from .fields import Field

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        for key in fields.keys():
            attrs.pop(key)
        attrs['_fields'] = fields
        attrs['__slots__'] = list(fields.keys())
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self._fields:
                raise ValueError(f"Unknown field: {key}")
            if key in self.__slots__:
                object.__setattr__(self, key, value)
            else:
                setattr(self, key, value)

    def save(self, session):
        session.add(self)

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def filter(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).all()

    @classmethod
    def first(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).first()
