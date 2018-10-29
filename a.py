class Event(object):
    def __init__(self):
        self.pool = {}
    def on(event, callback):
        if self.pool[event] is None:self.pool[event] = []
        self.pool[event].append(callback)
        return self
    def emit(event,*args,**keywords):
        if self.pool[event]:
            for fn in self.pool[event]:
                fn(*args,**keywords)

event = Event()

if __name__  == "__main__":
    event.on("data",lambda data:print(data))
    event.emit("data",{"name":"dpf","age":18})






