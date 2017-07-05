#!/bin/bash
_now=$(date +"%m_%d_%Y")
_file="$_now.dat"
python manage.py printmodels 2> "$_file"