import argparse
import json
import re


from random import randint

# Maximum number of levels deep we should go on embedded random tables
MAX_DEPTH = 30

# Keywords that have special meaning and should be ignored by parse_and_replace()
RESTRICTED_KEYWORDS = [
    "RANDOM_HEX",
    "NAMED_NPC",
    "NAMED_FRIENDLY_NPC",
    "NAMED_ENEMY_NPC"
]


def parse_and_replace(text, tables, depth=0, max_depth=MAX_DEPTH):
    """
    Parses the text for the first instance of a {{TABLE_REFERENCE}} and replaces it with the result from that table

    Returns the updated string, or the original text if no {{TABLE_REFERENCE[s]}} found
    """
    if depth > max_depth:
        return text
    updated_text = text
    table_references = re.findall(r"{{([A-Za-z0-9_]+)}}", updated_text)
    for table_name in table_references:
        if table_name not in RESTRICTED_KEYWORDS:
            table_text = roll_on_table(tables[table_name])
            # Dive down into the new table result to look for more TABLE_REFERENCE[s]
            table_text = parse_and_replace(table_text, tables, depth=depth + 1)
            updated_text = updated_text.replace(r"{{" + table_name + r"}}", table_text, 1)
    return updated_text


def roll_on_table(table):
    """
    Fetch a random entry from the given table

    If the table is a list, simply return a random entry

    If the table is a dict, roll dice and lookup result
    """
    if type(table) is list:
        return table[randint(0, len(table)) - 1]
    if type(table) is dict:
        results = sorted([int(key) for key in table.keys()])
        max_roll = results[-1]
        roll = randint(1, max_roll)
        for result in results:
            if roll <= result:
                return table[str(result)]


def load_npcs(npcs, tables):
    """
    Go through all the provided NPCs, parses their seed strings
    """
    named_npcs = {}
    if type(npcs) is list:
        key = 1
        for npc in npcs:
            named_npcs[str(key)] = {
                "name": parse_and_replace(npc["name"], tables),
                "description": parse_and_replace(npc["description"], tables),
                "references": [],
                "key": str(key)
            }
            key += 1
    if type(npcs) is dict:
        for key, npc in npcs.iteritems():
            named_npcs[str(key)] = {
                "name": parse_and_replace(npc["name"], tables),
                "description": parse_and_replace(npc["description"], tables),
                "references": [],
                "key": str(key)
            }
    return named_npcs


def set_named_npcs(hex_contents, named_npcs):
    """
    Goes through all hexes, finds references to {{NAMED_NPC}}, replaces them with a random entry from named_npcs, ands adds a reference to the npc
    """
    for k, v in hex_contents.iteritems():
        npc_references = re.findall(r"{{NAMED_NPC}}", v["text"])
        for npc_reference in npc_references:
            npc = roll_on_table(named_npcs)
            hex_contents[k]["text"] = hex_contents[k]["text"].replace(r"{{NAMED_NPC}}", npc["name"], 1)
            named_npcs[npc["key"]]["references"].append(k)
    return hex_contents


def set_random_hexes(hex_contents):
    """
    Goes through all records in the hexmap, finds references to {{RANDOM_HEX}}, replaces them with the hex number, and adds a reference on the random hex
    """
    updated_hex_contents = hex_contents
    hexes = hex_contents.keys()
    for k, v in hex_contents.iteritems():
        hex_references = re.findall(r"{{RANDOM_HEX}}", v["text"])
        for hex_reference in hex_references:
            random_hex = k
            while random_hex == k:
                random_hex = roll_on_table(hexes)
            updated_hex_contents[k]["text"] = hex_contents[k]["text"].replace(r"{{RANDOM_HEX}}", random_hex, 1)
            updated_hex_contents[random_hex]["references"].append(k)
    return updated_hex_contents


def populate_hex_contents(hexmap, tables):
    hex_contents = {}
    for k, v in hexmap.iteritems():
        hex_contents[k] = {"text": parse_and_replace(v, tables), "references": []}
    return set_random_hexes(hex_contents)


def print_hex_contents(hex_contents):
    for key in sorted(hex_contents.keys()):
        print(u"{0}".format(key))
        print(u"{0}".format(hex_contents[key]["text"]))
        if hex_contents[key]["references"]:
            print(u"SEE: {0}".format(", ".join(sorted(hex_contents[key]["references"]))))
        print


def print_named_npcs(named_npcs):
    # Sort by name
    for named_npc in sorted(named_npcs.items(), key=lambda x: x[1]["name"]):
        print(u"{0}".format(named_npc[1]["name"]))
        if named_npc[1]["description"]:
            print(u"{0}".format(named_npc[1]["description"]))
        if named_npc[1]["references"]:
            print(u"SEE: {0}".format(", ".join(sorted(list(set(named_npc[1]["references"]))))))
        print


def print_hex_contents_html(hex_contents):
    print(u"<div class=\"hexes\">")
    for key in sorted(hex_contents.keys()):
        print(u"<div class=\"hex\">\n<h1>{0}</h1>".format(key))
        print(u"{0}".format(hex_contents[key]["text"]))
        if hex_contents[key]["references"]:
            print(u"<h2>See {0}</h2>".format(", ".join(sorted(hex_contents[key]["references"]))))
        print(u"</div>")
    print(u"</div>")


def print_named_npcs_html(named_npcs):
    print(u"<div class=\"named_npcs\">")
    # Sort by name
    for named_npc in sorted(named_npcs.items(), key=lambda x: x[1]["name"]):
        print(u"<div class=\"named_npc\">\n<h2>{0}</h2>".format(named_npc[1]["name"]))
        if named_npc[1]["description"]:
            print(u"<p>{0}</p>".format(named_npc[1]["description"]))
        if named_npc[1]["references"]:
            print(u"<p>See {0}<p>".format(", ".join(sorted(list(set(named_npc[1]["references"]))))))
        print(u"</div>")
    print(u"</div>")


def print_hexpop_html(hex_contents, named_npcs={}):
    print(u"<div class=\"hexpop\">")
    print_hex_contents_html(hex_contents)
    print_named_npcs_html(named_npcs)
    print(u"</div>")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--npcs")
    parser.add_argument("hexmap")
    parser.add_argument("tables")
    args = parser.parse_args()

    with open(args.hexmap, "r") as f:
        hexmap = json.load(f)

    with open(args.tables, "r") as f:
        tables = json.load(f)

    named_npcs = {}
    if args.npcs:
        with open(args.npcs, "r") as f:
            npcs = json.load(f)
            named_npcs = load_npcs(npcs, tables)

    hex_contents = populate_hex_contents(hexmap, tables)

    if args.npcs:
        hex_contents = set_named_npcs(hex_contents, named_npcs)

    print_hexpop_html(hex_contents, named_npcs)


if __name__ == "__main__":
    main()
