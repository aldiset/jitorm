from .jit_mapping import map_to_instance

class Query:
    def __init__(self, model_class, session):
        self.model_class = model_class
        self.session = session
        self.filters = {}
        self._results = None

    def filter(self, **kwargs):
        self.filters.update(kwargs)
        return self

    def _build_query(self):
        query = f"SELECT * FROM {self.model_class.__name__.lower()}"
        if self.filters:
            filter_clauses = [f"{key} = ?" for key in self.filters.keys()]
            query += " WHERE " + " AND ".join(filter_clauses)
        return query, list(self.filters.values())

    def _execute_query(self):
        if self._results is None:
            query, params = self._build_query()
            self.session.storage.connect()  # Ensure the connection is open
            cursor = self.session.storage.conn.cursor()  # Create a cursor directly
            try:
                cursor.execute(query, params)  # Execute the query
                rows = cursor.fetchall()  # Fetch all rows
                self._results = [map_to_instance(self.model_class, row) for row in rows]
            finally:
                cursor.close()  # Always close the cursor
                self.session.storage.close()  # Close the connection to release resources

        return self._results

    def all(self):
        return self._execute_query()

    def first(self):
        results = self._execute_query()
        return results[0] if results else None
