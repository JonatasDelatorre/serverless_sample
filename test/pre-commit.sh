#!/bin/sh
coverage run -m pytest test/conftest.py
coverage report --fail-under=60