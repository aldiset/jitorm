from .fields import Field

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        attrs['_fields'] = fields 
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self._fields:
                raise ValueError(f"Unknown field: {key}")
            setattr(self, key, value) 

    def save(self, session):
        session.add(self)

    def __repr__(self):
        field_values = ", ".join(f"{k}={getattr(self, k)}" for k in self._fields.keys())
        return f"<{self.__class__.__name__}({field_values})>"

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def filter(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).all()

    @classmethod
    def first(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).first()
