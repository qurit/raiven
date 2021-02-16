from api.database import SessionLocal


class DatabaseService:
    def __init__(self):
        self._db = None

    def __enter__(self):
        """ Contextmanager to handle database connection """
        self._db = SessionLocal()
        return self

    def __exit__(self, *args):
        try:
            self._db.commit()
        finally:
            self._db.close()
            self._db = None
