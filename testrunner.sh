#!/usr/bin/env bash

export PYTHONPATH="${PYTHONPATH}:/${PWD}"

# More configuration needed ??
#export HB=$(brew --prefix)
#export QGIS_HB_PREFIX=${HB}/opt/qgis2
#export QGIS_BUNDLE=${QGIS_HB_PREFIX}/QGIS.app/Contents
#export QGIS_PREFIX_PATH=${QGIS_BUNDLE}/MacOS
#export PATH=${QGIS_PREFIX_PATH}/bin:$PATH
#export PYTHONPATH=${QGIS_HB_PREFIX}/lib/python2.7/site-packages:${HB}/opt/gdal2-python/lib/python2.7/site-packages:${HB}/lib/python2.7/site-packages:$PYTHONPATH
#export GDAL_DRIVER_PATH=${HB}/lib/gdalplugins
#export GDAL_DATA=${HB}/opt/gdal2/share/gdal
#export GRASS_PREFIX=${HB}/opt/grass7/grass-base


/usr/bin/python3 test/test_pass.py
/usr/bin/python3 test/test_init.py
/usr/bin/python3 test/test_translations.py
/usr/bin/python3 test/test_qgis_environment.py
/usr/bin/python3 test/test_resources.py

