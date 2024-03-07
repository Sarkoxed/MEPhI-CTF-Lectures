d = var('d')
P = PolynomialRing(GF(q), d)
d = P(d)

ks = [P(hi  + ri * d) * pow(si, -1, q) for hi, ri, si in triplets]

M = Matrix(P, [[pow(k, i) for i in range(t)] for k in ks[:-2]])
V = vector(P, ks[1:-1])
T = M.solve_right(V)
den = M.det()

final_poly = P(ks[-1] * den - den * sum(T[i] * ks[-2]**i for i in range(t)))
final_poly.roots()
