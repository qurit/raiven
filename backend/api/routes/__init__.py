from api import api

from .modalities import api as ns_api
from .jobs import api as ns_jobs

api.add_namespace(ns_api)
api.add_namespace(ns_jobs)
