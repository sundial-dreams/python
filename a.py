<<<<<<< HEAD
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
=======
import types
def G(n:int):
    a = [1]
    b = [1,1]
    while n:
        done = yield a
        if done: return
        a = b
        b = [1 if i==0 or i==len(a)-1 else a[i-1] + a[i] for i in range(len(a)+1)]


if __name__  == "__main__":
    for x in G(10):
        print(*x)














>>>>>>> dev






