class Events:
    'class for storing events in heap'
    e_id = 0

    def __init__(self, msg, time):
        self.msg = msg
        self.time = time
        Events.e_id +=1

    def __lt__(self,other):
        val = self.time
        otherval = other.time
        return val < otherval

    def get_event(self):
        return self.msg
    
