import random
import string
import hashlib
import json
import os
from datetime import datetime

ABS_PATH = os.path.dirname(__file__)
TOKENS_PATH = ABS_PATH + '/../data/tokens.json'

# Generate a random string of length 20
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

# Create a hash of the random string using SHA-256
hash_value = hashlib.sha256(random_string.encode()).hexdigest()

# Print the random string and the hash
print('Random String:', random_string)
print('Hash:', hash_value)

# Create a JSON object with the date and the hash
data = {
    "date": datetime.now().isoformat(),
    "hash": hash_value
}

if not os.path.exists(TOKENS_PATH):
    # Create tokens.json file if it doesn't exist
    with open(TOKENS_PATH, 'w') as file:
        json.dump([], file)

# Load the existing JSON list from tokens.json
with open(TOKENS_PATH, 'r') as file:
    json_list = json.load(file)

# Append the new JSON object to the end of the JSON list
json_list.append(data)

# Write the updated JSON list back to tokens.json
with open(TOKENS_PATH, 'w') as file:
    json.dump(json_list, file, indent=4)


