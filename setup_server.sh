#!/bin/sh

chown -R pi:www-data ./

find . -name "ods.pdf" -exec rm -f {} \;
find . -name "ods.log" -exec rm -f {} \;
find . -name "*.tex" -exec chmod 664 {} \;
