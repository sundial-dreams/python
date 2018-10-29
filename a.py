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




















