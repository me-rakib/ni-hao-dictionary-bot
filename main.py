import json
from difflib import get_close_matches

data = json.load(open("data.json"))

def meaning(w):
    keys = data.keys()
    close_match = get_close_matches(w, keys)
    if w in keys:
        return data[w]
    elif w.title() in keys:
        return data[w.title()]
    elif w.upper() in keys:
        return data[w.upper()]
    elif len(close_match) >= 1:
        return f"Maybe you meant '{close_match[0]}' which means '{data[close_match[0]][0]}'"
    else:
        return "My bad! This might be a new word!"

word = input("Enter word: ").lower()
output = meaning(word)
if type(output) == list:
    print(output[0])
else:
    print(output)
