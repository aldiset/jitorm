class Field:
    def __init__(self, primary_key=False):
        self.primary_key = primary_key

class IntegerField(Field):
    def __init__(self, primary_key=False):
        super().__init__(primary_key)
        self.auto_increment = primary_key

class StringField(Field):
    def __init__(self, primary_key=False):
        super().__init__(primary_key)

class AutoField(IntegerField):
    def __init__(self):
        super().__init__(primary_key=True)
