import jit_wrapper
from package.runtime import main

class Query:
    def __init__(self, model_class, session):
        self.model_class = model_class
        self.session = session
        self.filters = {}
        self.compile = main()

    def filter(self, **kwargs):
        self.filters.update(kwargs)
        return self

    def all(self):
        query = f"SELECT * FROM {self.model_class.__name__.lower()}"
        if self.filters:
            filter_clauses = [f"{key} = ?" for key in self.filters.keys()]
            query += " WHERE " + " AND ".join(filter_clauses)
            params = list(self.filters.values())
        else:
            params = []

        rows = self.session.storage.execute(query, params).fetchall()
        return [jit_wrapper.map_to_instance(self.model_class, row) for row in rows]

    def first(self):
        results = self.all()
        return results[0] if results else None
