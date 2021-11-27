LOG = open("applepy.log", "w")

def signed(x):
    if x > 0x7F:
        x = x - 0x100
    return x
