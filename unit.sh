#!/bin/sh
pip install nose mock==2.0 coverage pep8 unittest2 testfixtures
bash ./unit_run.sh
pep8 --ignore E501 st_engine > pep8.out || true
