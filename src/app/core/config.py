#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Setting up variables from .env file
"""
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

import secrets, os
from typing import Any, Dict, List, Optional, Union
import os
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    SERVER_NAME: str
    SERVER_HOST: str = AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost", "http://localhost:8888"]
    WORK_ENVIRONMENT: str

    # Using Pydantic validator decorators it’s possible to validate config fields using functions.
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
        
    # Behaviour of pydantic can be controlled via the Config class on a model, we specify that our settings are case-sensitive.
    class Config:
        case_sensitive = True

settings = Settings()

