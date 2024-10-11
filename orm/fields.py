class Field:
    def __init__(self, field_type, primary_key=False):
        self.field_type = field_type
        self.primary_key = primary_key


class IntegerField(Field):
    def __init__(self, primary_key=False):
        super().__init__(int, primary_key)


class StringField(Field):
    def __init__(self, primary_key=False):
        super().__init__(str, primary_key)
        

class BooleanField(Field):
    def __init__(self, primary_key=False):
        super().__init__(bool, primary_key)

