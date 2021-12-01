#!/bin/sh
coverage run --include=src/extract.py,src/process.py -m pytest test/etl_test.py
coverage report --fail-under=60