import argparse
import json
import re


from random import randint

# Maximum number of levels deep we should go on embedded random tables
MAX_DEPTH = 20

# Keywords that have special meaning and should be ignored by parse_and_replace()
RESTRICTED_KEYWORDS = [
    "RANDOM_HEX",
    "NAMED",
    "FIRST_NAME",
    "LAST_NAME",
    "IMPORTANT_NPC"
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


def set_random_hex(hex_contents):
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

    hex_contents = set_random_hex(hex_contents)

    return hex_contents


def print_hex_contents(hex_contents):
    for key in sorted(hex_contents.keys()):
        print(u"{0}: {1}".format(key, hex_contents[key]["text"]))
        if hex_contents[key]["references"]:
            print(u"SEE: {0}".format(", ".join(sorted(hex_contents[key]["references"]))))
        print


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hexmap")
    parser.add_argument("tables")
    args = parser.parse_args()

    with open(args.hexmap, "r") as f:
        hexmap = json.load(f)

    with open(args.tables, "r") as f:
        tables = json.load(f)

    hex_contents = populate_hex_contents(hexmap, tables)

    print_hex_contents(hex_contents)


if __name__ == "__main__":
    main()
