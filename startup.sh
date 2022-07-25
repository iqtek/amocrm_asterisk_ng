#! /bin/bash

# Single application launch point.

source ./venv/bin/activate
uvicorn amocrm_asterisk_ng:app --host 0.0.0.0 --port 8000
