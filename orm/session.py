from .query import Query
from .fields import Field

class Session:
    def __init__(self, storage):
        self.storage = storage
        self._transaction = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def add(self, model):
        """Add a new record to the database and return the inserted data."""
        fields = ', '.join([f for f in model._fields if getattr(model, f) is not None])
        values = tuple(getattr(model, f) for f in model._fields if getattr(model, f) is not None)
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {model.__class__.__name__.lower()} ({fields}) VALUES ({placeholders})"
        
        with self.storage.execute(query, values) as cursor:
            self.commit()
            last_row_id = cursor.lastrowid
        return self.refresh(model, last_row_id)

    def commit(self):
        self.storage.commit()
        self._transaction.clear()

    def rollback(self):
        self._transaction.clear()

    def query(self, model_class):
        return Query(model_class, self)

    def bulk_create(self, model, items):
        columns = ', '.join(items[0].keys())
        placeholders = ', '.join(['?' for _ in items[0]])
        query = f"INSERT INTO {model.__name__.lower()} ({columns}) VALUES ({placeholders})"
        params = [tuple(item.values()) for item in items]
        breakpoint()
        self.storage.executemany(query, params)
        self.commit()

    def bulk_update(self, datas):
        if not datas:
            return

        model_class = datas[0].__class__
        pk_field = None
        for field, attr in vars(model_class).items():
            if isinstance(attr, Field) and attr.primary_key:
                pk_field = field
                break

        if not pk_field:
            raise ValueError(f"No primary key defined for {model_class.__name__}")

        # Collect updates by their set clause to minimize the number of different SQL commands
        updates = {}
        for model in datas:
            set_parts = []
            params = []
            for field, value in vars(model).items():
                if field != pk_field and value is not None:
                    set_parts.append(f"{field} = ?")
                    params.append(value)
            if set_parts:
                set_clause = ', '.join(set_parts)
                key_value = getattr(model, pk_field)
                # Group updates by their SQL to minimize preparation of statements
                if set_clause not in updates:
                    updates[set_clause] = []
                updates[set_clause].append(tuple(params + [key_value]))  # Add PK value last

        self.storage.execute("BEGIN TRANSACTION;")
        for set_clause, all_params in updates.items():
            query = f"UPDATE {model_class.__name__.lower()} SET {set_clause} WHERE {pk_field} = ?;"
            self.storage.executemany(query, all_params)
        self.storage.execute("COMMIT;")
        return


    def update(self, model_class, filters, **kwargs):
        set_clause = ', '.join([f"{key} = ?" for key in kwargs])
        filter_clause = ' AND '.join([f"{key} = ?" for key in filters])
        query = f"UPDATE {model_class.__name__.lower()} SET {set_clause} WHERE {filter_clause}"
        params = list(kwargs.values()) + list(filters.values())
        self.storage.execute(query, params)
        self.storage.commit()

    def delete(self, model_class, filters):
        filter_clauses = ' AND '.join([f"{key} = ?" for key in filters])
        params = list(filters.values())
        query = f"DELETE FROM {model_class.__name__.lower()} WHERE {filter_clauses}"
        self.storage.execute(query, params)
        self.storage.commit()

    def refresh(self, model, last_row_id):
        """Refresh and return the model's data from the database using the last inserted row ID."""
        pk_field = next((f for f in model._fields if getattr(model._fields[f], 'primary_key', False)), None)
        if not pk_field:
            raise ValueError("No primary key defined for the model.")
        
        query = f"SELECT * FROM {model.__class__.__name__.lower()} WHERE {pk_field} = ?"
        with self.storage.execute(query, (last_row_id,)) as cursor:
            row = cursor.fetchone()
            if row:
                for field in model._fields:
                    setattr(model, field, row[field])
        return model


