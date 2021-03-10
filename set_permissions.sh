#!/bin/sh
chown -R pi:www-data ./
find . -name ".tex" -exec chmod 664 {} \;
