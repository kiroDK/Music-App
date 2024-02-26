import random

def randomnumber():
    num = random.randrange(1000,9999)
    return num


def randomalphanum():
    charvalue="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    s=""
    for i in range(1,5):
        index = random.randrange(0,36)
        s=s+charvalue[index]
    return s