class BaseState(object):
    """Implements the base class to the other states"""
    
    def __init__(self):
        self.done = False
        self.state_name = None
        self.next_state = None
        self.previous_state = None
        self.site = None

    def startup(self, site = None):
        pass

    def get_event(self, event):
        pass

    def get_name(self):
        return self.state_name

    def get_next_state(self):
        return self.next_state

    def put_previous_state(self, state_name):
        self.previous_state = state_name

    def update_site(self, site):
        self.site = site

    def get_site(self):
        return self.site

    
