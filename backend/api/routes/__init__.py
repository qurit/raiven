from api import api

# from .modalities import api as ns_api
# from .jobs import api as ns_jobs
# from .containers import api as ns_containers
from .auth import api as ns_auth
from .application_entity import api as ns_application_entity

# api.add_namespace(ns_api)
# api.add_namespace(ns_jobs)
# api.add_namespace(ns_containers)
api.add_namespace(ns_auth)
api.add_namespace(ns_application_entity)
