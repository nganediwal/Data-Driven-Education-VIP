#!/bin/bash

mongo -u edx_vip_students -p edx_data_access@C21U 34.193.51.227/edx --quiet mongodb/attributes.js > temp.json
python mongodb/attributes.py temp.json $1

rm temp.json