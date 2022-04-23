def S_t(t):
    s = 290797
    n = 0
    while n <= 4*t - 1:
        yield s
        s = (s ** 2) % 50515093
        n += 1

