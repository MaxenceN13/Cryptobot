from user import User
import jsonpickle

class Users:
    def __init__(self):
        self.users = {}
    
    def add(self, user : User):
        self.users[user.id] = user
    
    def remove(self, user_id):
        self.users.pop(user_id)
    
    def get(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        return None
    
    def exist(self, user_id):
        return user_id in self.users.keys()

    def save(self, path):
        users_json = jsonpickle.encode(self.users)
        with open(path, "w") as file:
            file.write(users_json)
        
    def load(self, path):
        # key have to be int
        # dictionary keys changed during iteration
        with open(path, "r") as file:
            self.users = jsonpickle.decode(file.read())
            for k in list(self.users.keys()):
                self.users[int(k)] = self.users.pop(k)

    def __str__(self):
        r = ""
        for (k,v) in self.users.items():
            r +="{} : {}\n".format(k, v)
        return r