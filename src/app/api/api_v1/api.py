#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Assigning route of API and registering different APIS """
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

from fastapi import APIRouter
from app.api.api_v1.endpoints import ner

api_router = APIRouter()

api_router.include_router(ner.router, prefix="/entity-recognition", tags=["ner"])
