#!/usr/bin/python3
"""
    Init
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.demo import *
from api.v1.views.vitals import *
from api.v1.views.complaint import *
from api.v1.views.diagnosis import *
from api.v1.views.medics import *
from api.v1.views.procedure import *
from api.v1.views.plan import *
from api.v1.views.plan_proc import *
