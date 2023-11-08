#!/usr/bin/env bash

virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/personal_cab/requirements.txt
cd /home/ubuntu/env/bin
pip install gunicorn
