def nontrivial(l):
    if type(l) == list:
        return [i for i in l if i]
    else:
        return (i for i in iter(l) if i)

def str_or_else(s, or_else=""):
    return str(s) if s else or_else