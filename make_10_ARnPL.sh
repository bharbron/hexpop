#!/bin/bash 
COUNTER=1
RUNTIME=$(date +%s)
while [  $COUNTER -lt 11 ]; do
	echo $COUNTER of 10
	FILENAME="ARnPL_${RUNTIME}_${COUNTER}.html"
	echo $FILENAME
	python hexpop.py --npcs ARnPL_npcs.json ARnPL_map.json ARnPL_tables.json > ${FILENAME}
	echo "Adventure Hooks (<div class=\"adventure_hook\">)"
	grep -o "<div class=\"adventure_hook\">" ${FILENAME} | wc -l
	echo "Total Landmarks (<h3>)"
	grep -o "<h3>" ${FILENAME} | wc -l
	echo "Day Encounters (<strong>day)"
	grep -o "<strong>day" ${FILENAME} | wc -l
	echo "Night Encounters (<strong>night)"
	grep -o "<strong>night" ${FILENAME} | wc -l
	echo "Interior Encounters (<div class=\"interior_encounter\">)"
	grep -o "<div class=\"interior_encounter\">" ${FILENAME} | wc -l
	echo "NPCs carrying items (Carrying)"
	grep -p "Carrying" ${FILENAME} | wc -l
	echo "All Treasures (<div class=\"treasure\">)"
	grep -o "<div class=\"treasure\">" ${FILENAME} | wc -l
	echo "Spellbooks (<p>Contains Spell) [only in treasures]"
	grep -o "<p>Contains Spell" ${FILENAME} | wc -l
	echo "Magical Items (<p>Contains magical)"
	grep -o "<p>Contains magical" ${FILENAME} | wc -l
	echo "Rare Treasures (<p>Contains rare)"
	grep -o "<p>Contains rare" ${FILENAME} | wc -l
	echo "Coins or Jewelry (<p>Contains coins) [only in treasures]"
	grep -o "<p>Contains coins" ${FILENAME} | wc -l
	echo "All Spellbooks (Spell)"
	grep -o "Spell" ${FILENAME} | wc -l
	echo "Hex references (<strong>square)"
	grep -o "<strong>square" ${FILENAME} | wc -l
	echo "Referenced hexes (<h2>See)"
	grep -o "<h2>See" ${FILENAME} | wc -l

    let COUNTER=COUNTER+1 
 done