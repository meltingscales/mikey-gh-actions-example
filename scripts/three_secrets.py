import os
from pprint import pprint
import json

secret_names = [
    'SECRET_ONE',
    'SECRET_TWO',
    'SECRET_THREE',
    'ALL_SECRETS', # note that this one is a json string blob
]

def does_look_like_json(s:str)->bool:
    """Attempts to parse the string as json and returns True if successful."""
    try:
        json.loads(s)
        return True
    except:
        return False

secret_dict = dict()

for secret_name in secret_names:
    secret_dict[secret_name] = os.getenv(secret_name)

    if does_look_like_json(secret_dict[secret_name]):
        secret_dict[secret_name] = json.loads(secret_dict[secret_name])
        for k,v in secret_dict[secret_name].items():
            print("potato1 "+k+" "+v)
    else:
        secret_dict[secret_name] = secret_dict[secret_name]
        print("potato2 "+ secret_dict[secret_name])

pprint(secret_dict)