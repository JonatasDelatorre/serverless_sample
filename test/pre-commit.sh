#!/bin/sh
coverage run -m pytest test/etl_test.py
coverage report --fail-under=60