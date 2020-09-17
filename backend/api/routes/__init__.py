from api import api

# from .modalities import api as ns_api
# from .jobs import api as ns_jobs
from .auth import api as ns_auth
# from .containers import api as ns_containers

# api.add_namespace(ns_api)
# api.add_namespace(ns_jobs)
api.add_namespace(ns_auth)
# api.add_namespace(ns_containers)
