#! /bin/bash

sudo -u postgres dropdb saleor
sudo -u postgres createdb -O saleor saleor
python3 manage.py migrate
