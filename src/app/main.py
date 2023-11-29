#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Main file to run the fast API,
    Set fast API app
    Set all CORS enabled origins,
    initialize LOGs """
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.common.logger import LOG

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


LOG.init()
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS], # list of origins to make cross-origin requests
        allow_credentials=True, # indicate that cookies should be supported for cross origin requests
        allow_methods=["*"], # list of http methods allowed for cross-origin requests
        allow_headers=["*"], # list of http headers supported for cross origin requests
    )

app.include_router(api_router, prefix=settings.API_V1_STR)