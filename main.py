import re

from random import randint

# Maximum number of levels deep we should go on embedded random tables
MAX_DEPTH = 3

# Keywords that have special meaning and should be ignored by parse_and_replace()
RESTRICTED_KEYWORDS = [
    "RANDOM_HEX"
]

def parse_and_replace(text, tables, depth=0, max_depth=MAX_DEPTH):
    """
    Parses the text for the first instance of a {{TABLE_REFERENCE}} and replaces it with the result from that table

    Returns the updated string, or the original text if no {{TABLE_REFERENCE[s]}} found
    """
#    print "depth = {0}".format(depth)
#    print "max_depth = {0}".format(max_depth)
    if depth >= max_depth:
#        print "too deep"
        return text
#    print "text = {0}".format(text)
    table_references = re.search(r"{{([A-Za-z0-9_]+)}}", text)
#    print "table_references = {0}".format(table_references)
    if table_references:
        table_name = table_references.group(1)

        # TODO: Fix this so it will loop until finding the first non-restricted keyword
        if table_name not in RESTRICTED_KEYWORDS:
            table_text = roll_on_table(tables[table_name])
            # Dive down into the new table result to look for more TABLE_REFERENCE[s]
            table_text = parse_and_replace(table_text, tables, depth=depth+1)
            updated_text = re.sub(r"{{[A-Za-z0-9_]+}}", table_text, text, count=1)
            # Continue across the same text to find more TABLE_REFERENCES[s] at the same depth
            return parse_and_replace(updated_text, tables, depth=depth)
        else:
            return parse_and_replace(text, tables, depth=depth)
    else:
        return text

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
#        print "results = {0}".format(results)
        max_roll = results[-1]
        roll = randint(1, max_roll)
        for result in results:
            if roll <= result:
                return table[str(result)]