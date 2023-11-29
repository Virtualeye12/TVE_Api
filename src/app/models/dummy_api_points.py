#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Input and Output for API, along with data types
"""
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

from pydantic import BaseModel
from typing import Optional
from typing import List


class ModelInput(BaseModel):
    message: str

class ModelOutput(BaseModel):
    msg: str
    user_message: str
    labels: List

