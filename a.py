class Event(object):
    def __init__(self):
        self.pool = {}
    
    
    def on(self,event, callback):
        if self.pool.get(event,None) is None:self.pool[event] = []
        self.pool[event].append(callback)
        return self
    
    def emit(self,event,*args,**keywords):
        if self.pool[event]:
            for fn in self.pool[event]:
                fn(*args,**keywords)

event = Event()

if __name__  == "__main__":
    event.on("data",lambda data:print(data))
    event.emit("data",{"name":"dpf","age":18})






