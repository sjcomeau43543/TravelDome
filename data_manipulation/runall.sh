#!/usr/bin/env bash
python3 merge.py -l ../scrapers/locations.txt
python3 storage.py -l ../scrapers/locations.txt -a ../scrapers/adjectives_extended.txt
python3 clustering.py -e ../scrapers/adjectives_extended.txt -n 5