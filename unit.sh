#!/bin/sh
pip install nose mock==2.0 coverage pep8 unittest2 testfixtures
bash ./unit_run.sh
pep8 --ignore E501 src > pep8.out || true