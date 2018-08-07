python hexpop.py --npcs ARnPL_npcs.json ARnPL_map.json ARnPL_tables.json > ARnPL_analyze.html
echo "Adventure Hooks (<p>&#9758;)"
grep -o "<p>&#9758;" ARnPL_analyze.html | wc -l
echo "Total Landmarks (<h3>)"
grep -o "<h3>" ARnPL_analyze.html | wc -l
echo "Day Encounters (<strong>day)"
grep -o "<strong>day" ARnPL_analyze.html | wc -l
echo "Night Encounters (<strong>night)"
grep -o "<strong>night" ARnPL_analyze.html | wc -l
echo "Interiors (<h3>Interior) [encounters roughly 1/2 this]"
grep -o "<h3>Interior" ARnPL_analyze.html | wc -l
echo "NPCs carrying items (Carrying)"
grep -p "Carrying" ARnPL_analyze.html | wc -l
echo "All Treasures (<p>Contains)"
grep -o "<p>Contains" ARnPL_analyze.html | wc -l
echo "Spellbooks (<p>Contains Spell) [only in treasures]"
grep -o "<p>Contains Spell" ARnPL_analyze.html | wc -l
echo "Magical Items (<p>Contains magical)"
grep -o "<p>Contains magical" ARnPL_analyze.html | wc -l
echo "Rare Treasures (<p>Contains rare)"
grep -o "<p>Contains rare" ARnPL_analyze.html | wc -l
echo "Coins or Jewelry (<p>Contains Coins) [only in treasures]"
grep -o "<p>Contains Coins" ARnPL_analyze.html | wc -l
echo "All Spellbooks (Spell)"
grep -o "Spell" ARnPL_analyze.html | wc -l
echo "Hex references (<strong>square)"
grep -o "<strong>square" ARnPL_analyze.html | wc -l
echo "Referenced hexes (<h2>See)"
grep -o "<h2>See" ARnPL_analyze.html | wc -l