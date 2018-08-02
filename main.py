from random import randint

# Maximum number of levels deep we should go on embedded random tables
MAX_DEPTH = 10

# Keywords that have special meaning and should be ignored by parse_and_replace()
RESTRICTED_KEYWORDS = [
	"RANDOM_HEX"
]

def parse_and_replace(text):
    """
    Parses the text for the first instance of a %TABLE_REFERNCE% and replaces it with the result from that table

    Returns the updated string, or NoneType if there were no %TABLE_REFERENCE%[s]
    """
    pass


def roll_on_table(table):
    """
    Fetch a random entry from the given table

    If the table is a list, simply return a random entry

    If the table is a dict, roll dice and lookup result
    """
    if type(table) is list:
    	return table[randint(0, len(table)) - 1]
    if type(table) is dict:
    	results = sorted(table.keys())
    	max_roll = results[-1]
    	roll = randint(1, max_roll)
    	for result in results:
    		if roll <= result:
    			return table.get(result)