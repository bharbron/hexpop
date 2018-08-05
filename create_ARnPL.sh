#!/bin/bash

python hexpop.py --npcs ARnPL_npcs.json ARnPL_map.json ARnPL_tables.json > ARnPL_hexpop.html && prince -s fell_english_hexpop_A5.css ARnPL_hexpop.html && open ARnPL_hexpop.pdf
