import os

class Session(object):
    """
    A Class to represent a python interpreter session

    Attributes:
        name: A name identifier for the session
        users: A list of the users allowed to run code in the session
        namespace: A dictionary containing the enviromental variables for the session
        path: A path to the file where the session will be stored

    Methods:
        add_user(user): Adds a user to the list
        remove_user(user): Removes a user from the list
        save_session(): Saves the current namespace to file
        delete_session(): Deletes the existing session file
        clear_session(): Clears the namespace
        run(input): Execute the input in the session

    """
    def __init__(self, name, user, channel):
        super().__init__()
        self.name = name
        self.users = [user]
        self.namespace = {}
        self.path = os.path.join('sessions', name)

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def save_session(self):
        with open(self.path, '+w') as f:
            f.write(self.namespace)

    def delete_session(self):
        os.remove(self.path)

    def clear_session(self):
        self.namespace = {}

    def run(self, input):
        exec(input, self.namespace)
        return "ok"
