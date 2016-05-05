
def ghex(addr):
    if addr is None:
        return None
    return hex(addr).strip("L")

def fhex(addr):
    try:
        return int(addr, 16)
    except AttributeError:
        return None
