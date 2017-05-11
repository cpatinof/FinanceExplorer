#!/bin/bash

# go to workdir
cd src/

# run gunicorn
exec gunicorn DjangoProject.wsgi -b 0.0.0.0:8001
