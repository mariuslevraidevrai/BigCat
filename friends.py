import json
import os

def add(name, IP):
    new_entry = {name: IP}
    
    path = "account/friends/friendsList.json"
    
    if not os.path.exists(path):
        data = {}
    else:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    if name not in data:
        data.update(new_entry)
        print(f"{name} was added to your friends!")
    else:
        print(f"{name} already exist in your friends.")
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


