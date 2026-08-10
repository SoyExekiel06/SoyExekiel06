def main(a, b):
    int(a)
    int(b)
    if not (a > 0 and b > 0):
        raise ValueError
    return a + b