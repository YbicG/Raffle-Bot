import json

class FileType():
    balance = "balance"
    roblox_accounts = "roblox_accounts"
    
class Bucket():
    def __init__(self, with_file: FileType) -> None:
        self.file_type = with_file
    
    def get_value(self, key):
        key = str(key)
        with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json") as file:
            data = file.read()
            json_data = json.loads(data)
            file.close()
            
            if key in json_data:
                return json_data[key], True
            else:
                return "", False

    def get_list(self):
        with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json") as file:
            data = file.read()
            json_data = json.loads(data)
            file.close()
            
        return json_data
    
    def set_value(self, key, value):
        key = str(key)
        with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json") as file:
            data = file.read()
            json_data = json.loads(data)
            
            if key in json_data:
                del json_data[key]
                
            json_data[key] = value
            
            json_data = json.dumps(json_data) 

            file.close()
            
            with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json", "w") as file:
                file.write(json_data)
                file.close()
    
    def manage_value(self, id, key, value):
        id = str(id)
        key = str(key)
        with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json") as file:
            data = file.read()
            json_data = json.loads(data)
            
            if key in json_data:
                del json_data[id][key]
                
            json_data[id][key] = value
            
            json_data = json.dumps(json_data) 

            file.close()
            
            with open(f"Discord Bots\\Raffle Bot\\Database\\{self.file_type}.json", "w") as file:
                file.write(json_data)
                file.close()

def check_taken(username):
    bucket = Bucket(FileType.roblox_accounts)
    usernames = bucket.get_list()

    for user in usernames:
        if usernames[user] == username:
            return True, user
    
    return False, None

def get_roblox_username(discord_id):
    bucket = Bucket(FileType.roblox_accounts)
    
    username, exists = bucket.get_value(discord_id)
    
    if exists:
        return username
    else:
        return None

def set_roblox_username(discord_id, roblox_username):
    is_taken, by_id = check_taken(roblox_username)
    
    if is_taken:
        return False, by_id
    
    bucket = Bucket(FileType.roblox_accounts)
    
    bucket.set_value(discord_id, roblox_username)
    
    bucket = Bucket(FileType.balance)
    
    bucket.manage_value(discord_id, "roblox_username", roblox_username)
    
    return True, None