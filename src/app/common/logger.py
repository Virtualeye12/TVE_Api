#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : 
# version ='1.0'
# ---------------------------------------------------------------------------
""" Creating Logs for the Project
    Automatically generated by the module of the caller
    Usage:
        >>> LOG.info('My message: %s', debug_str)
        13:12:43.673 - :<module>:1 - INFO - My message: hi
        >>> LOG('custom_name').debug('Another message')
        13:13:10.462 - custom_name - DEBUG - Another message
"""
# ---------------------------------------------------------------------------
"""tunable parameters: None"""
# ---------------------------------------------------------------------------

import inspect
import logging
import sys

from os.path import isfile

from .utils import load_commented_json, merge_dict
from os.path import join, dirname, expanduser
import requests

requests.packages.urllib3.disable_warnings()
from logging.handlers import RotatingFileHandler


def _make_log_method(fn):
    @classmethod
    def method(cls, *args, **kwargs):
        cls._log(fn, *args, **kwargs)

    method.__func__.__doc__ = fn.__doc__
    return method


class LOG:
    """
    Custom logger class that acts like logging.Logger
    The logger name is automatically generated by the module of the caller
    Usage:
        >>> LOG.debug('My message: %s', debug_str)
        13:12:43.673 - :<module>:1 - DEBUG - My message: hi
        >>> LOG('custom_name').debug('Another message')
        13:13:10.462 - custom_name - DEBUG - Another message
    """

    _custom_name = None
    handler = None
    level = None
    es_log_level = None

    # Copy actual logging methods from logging.Logger
    # Usage: LOG.debug(message)
    debug = _make_log_method(logging.Logger.debug)
    info = _make_log_method(logging.Logger.info)
    warning = _make_log_method(logging.Logger.warning)
    error = _make_log_method(logging.Logger.error)
    exception = _make_log_method(logging.Logger.exception)

    @classmethod
    def init(cls, *confs):
        if len(confs) > 0:
            config = {}
            for conf in confs:
                try:
                    merge_dict(config, load_commented_json(conf) if isfile(conf) else {})
                except Exception as e:
                    print('couldn\'t load {}: {}'.format(conf, str(e)))

            cls.level = logging.getLevelName(config.get('log_level', 'INFO'))
            cls.es_log_level = logging.getLevelName(config.get('es_log_level', 'INFO'))
        else:
            cls.level = logging.getLevelName('DEBUG')
            cls.es_log_level = logging.getLevelName('INFO')

        fmt = '%(asctime)s.%(msecs)03d - ' \
              '%(name)s - %(levelname)s - %(message)s'
        datefmt = '%H:%M:%S'
        formatter = logging.Formatter(fmt, datefmt)
        cls.handler = logging.StreamHandler(sys.stdout)
        cls.handler.setFormatter(formatter)
        cls.create_logger('')  # Enables logging in external modules

    @classmethod
    def create_logger(cls, name):
        logger = logging.getLogger(name)
        logger.propagate = False
        logger.addHandler(cls.handler)
        logger.setLevel(cls.level)

        es_logger = logging.getLogger('elasticsearch')
        es_logger.setLevel(cls.es_log_level)
        es_logger.propagate = False
        # es_handler = RotatingFileHandler('indexer.log', maxBytes=20000, backupCount=10)
        # es_logger.addHandler(es_handler)

        urllib_logger = logging.getLogger('urllib3')
        urllib_logger.setLevel(logging.CRITICAL)
        urllib_logger.propagate = False
        return logger

    def __init__(self, name):
        LOG._custom_name = name

    @classmethod
    def _log(cls, func, *args, **kwargs):
        if cls._custom_name is not None:
            name = cls._custom_name
            cls._custom_name = None
        else:
            # Stack:
            # [0] - _log()
            # [1] - debug(), info(), warning(), or error()
            # [2] - caller
            stack = inspect.stack()

            # Record:
            # [0] - frame object
            # [1] - filename
            # [2] - line number
            # [3] - function
            # ...
            record = stack[2]
            mod = inspect.getmodule(record[0])
            module_name = mod.__name__ if mod else ''
            name = module_name + ':' + record[3] + ':' + str(record[2])
        func(cls.create_logger(name), *args, **kwargs)
