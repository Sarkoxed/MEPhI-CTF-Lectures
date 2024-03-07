def bsgs(P, Q, n):
    m = floor(sqrt(n))
    precomp = {}
    P0 = P.curve()((0, 1, 0))
    for j in range(3 * m):
        precomp[P0] = j
        P0 += P
    mP = m * P
    Q0 = Q
    for i in range(3 * m):
        if Q0 in precomp:
            return i * m + precomp[Q0]
        Q0 -= mP
    return Null
