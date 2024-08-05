from .fields import Field, IntegerField

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        primary_keys = [key for key, field in fields.items() if field.primary_key]
        if not primary_keys:
            fields['id'] = IntegerField(primary_key=True)
        elif len(primary_keys) > 1:
            raise ValueError("Multiple primary key fields are not allowed")
        
        for key in list(fields.keys()):
            if key in attrs:
                attrs.pop(key)
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
        session.commit()

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def filter(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).all()

    @classmethod
    def first(cls, session, **kwargs):
        return session.query(cls).filter(**kwargs).first()
