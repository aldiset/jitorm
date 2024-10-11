from .query import Query

class Session:
    def __init__(self, storage):
        self.storage = storage
        self._transaction = []

    def add(self, instance):
        instance_dict = {field: getattr(instance, field) for field in instance._fields if field!="id"}
        columns = ', '.join(instance_dict.keys())
        placeholders = ', '.join(['?' for _ in instance_dict.values()])
        query = f"INSERT INTO {instance.__class__.__name__.lower()} ({columns}) VALUES ({placeholders})"
        self.storage.execute(query, list(instance_dict.values()))
        self._transaction.append(('add', instance))
        
        self.refresh(instance)

    def commit(self):
        self.storage.commit()
        self._transaction.clear()

    def rollback(self):
        self._transaction.clear()

    def query(self, model_class):
        return Query(model_class, self)

    def update(self, model_class, filters, **kwargs):
        query = self.query(model_class).filter(**filters)
        instances = query.all()
        for instance in instances:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
            filter_clause = ' AND '.join([f"{key} = ?" for key in filters.keys()])
            query = f"UPDATE {model_class.__name__.lower()} SET {set_clause} WHERE {filter_clause}"
            params = list(kwargs.values()) + list(filters.values())
            self.storage.execute(query, params)
            self._transaction.append(('update', instance))

    def delete(self, model_class, filters):
        query = self.query(model_class).filter(**filters)
        instances = query.all()
        for instance in instances:
            filter_clause = ' AND '.join([f"{key} = ?" for key in filters.keys()])
            query = f"DELETE FROM {model_class.__name__.lower()} WHERE {filter_clause}"
            params = list(filters.values())
            self.storage.execute(query, params)
            self._transaction.append(('delete', instance))

    def refresh(self, instance):
        table_name = instance.__class__.__name__.lower()
        query = f"SELECT * FROM {table_name} WHERE rowid = last_insert_rowid()"  # Untuk mendapatkan ID terakhir
        cursor = self.storage.execute(query)
        row = cursor.fetchone()
        
        if row:
            # Mengambil semua kolom dari hasil query
            fields = list(instance._fields.keys())
            for idx, field in enumerate(fields):
                setattr(instance, field, row[idx])

        return instance
