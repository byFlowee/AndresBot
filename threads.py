import threading
from AndresBot import sessions

class ThreadManager(object): # Or whatever we want to call it
    """ 
    """
    def __init__(self):
        self.sessions = {}

    async def run_code(self, input, user, channel):
        if channel not in self.sessions:
            return 'This channel does not have a running session.'
        elif user not in self.sessions[channel].users:
            return 'You do not have access to this session.'
        else:
            self.sessions[channel].run(input)
            
    async def start_session(self, name, user, channel):
        session = sessions.Session(name, user, channel)
        self.sessions[channel] = session
        return

    async def get_session_name(self, channel):
        return self.sessions[channel].name if channel in self.sessions else ''
    
    async def clear_session(self, user, channel):
        if channel not in self.sessions:
            return 'This channel does not have a running session.'
        elif user not in self.sessions[channel].users:
            return 'You do not have access to this session.'
        else:
            self.sessions[channel].clear_session()
            return
    
    async def delete_session(self, user, channel):
        if channel not in self.sessions:
            return 'This channel does not have a running session.'
        elif user not in self.sessions[channel].users:
            return 'You do not have access to this session.'
        else:
            self.sessions[channel].delete_session()
            del self.sessions[channel]
            return
    