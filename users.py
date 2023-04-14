from user import User
import jsonpickle

class Users:
    def __init__(self):
        self.users = {}
        self.save_path = None
    
    def add(self, user : User):
        self.users[user.id] = user
    
    def remove(self, user_id):
        self.users.pop(user_id)
    
    def get(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        return None
    
    def exists(self, user_id):
        return user_id in self.users.keys()

    def save(self):
        users_json = jsonpickle.encode(self.users)
        with open(self.save_path, "w") as file:
            file.write(users_json)
        
    def load(self):
        with open(self.save_path, "r") as file:
            self.users = jsonpickle.decode(file.read())
            # make copy of keys to avoid RuntimeError: dictionary changed during iteration
            for k in list(self.users.keys()):
                self.users[int(k)] = self.users.pop(k)
            
    def setSavePath(self, path):
        self.save_path = path

    def __str__(self):
        r = ""
        for (k,v) in self.users.items():
            r +="{} : {}\n".format(k, v)
        return r