from api import worker_session

from . import populate


def run_startup_scripts():
    with worker_session() as db:
        populate.pre_populate_internal(db)

        db.commit()
