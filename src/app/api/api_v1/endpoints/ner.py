#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Testing
    Testing API: Test the API is working or not
"""
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

from fastapi import APIRouter, Body, Depends, HTTPException
from app.models import dummy_api_points
from app.common.logger import LOG

router = APIRouter()

@router.post("/test",  response_model=dummy_api_points.ModelOutput)
def testing_api(data: dummy_api_points.ModelInput):
    """
    Function : test api;
    Input : message text;
    Output : msg: str <success>;
             user_message: input msg;
             labels: ner label
    """
    LOG.info('testing api parsing')
    return {"msg": "success",
            "user_message": data.message,
            "labels": ['action','question']}

