import struct
from math import sin, floor

rotl = lambda x, k: ((x << k) | (x >> (32 - k))) & (2**32 - 1)
rotr = lambda x, k: rotl(x, 32 - k)


init = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
h = init.copy()
s = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

f = []
f.append(lambda B, C, D: (B & C) | (~B & D))
f.append(lambda B, C, D: (B & D) | (~D & C))
f.append(lambda B, C, D: B ^ C ^ D)
f.append(lambda B, C, D: C ^ (B | ~D))

w = []
w.append(lambda state, i: state[i])
w.append(lambda state, i: state[(5 * i + 1) % 16])
w.append(lambda state, i: state[(3 * i + 5) % 16])
w.append(lambda state, i: state[7 * i % 16])

t = [floor(2**32 * abs(sin(i))) for i in range(1, 65)]

def compress(self, block: bytes):
    state = struct.unpack("<16I", block)

    a, b, c, d = self.h

    for i in range(64):
        fi = self.f[i // 16](b, c, d)
        wi = self.w[i // 16](state, i)
        ti = self.t[i]
        si = self.s[i]

        q = b + rotl((a + fi + wi + ti) % 2**32, si)

        a, b, c, d = d, q % 2**32, b, c

    self.h = [(x + y) % 2**32 for x, y in zip([a, b, c, d], self.h)]

def digest(tail):
    block = tail
    length += len(block) * 8
    block += b"\x80"
    while len(block) % 64 != 56:
        block += b"\x00"
    
    block += struct.pack(b"<Q", self.length)
    compress
    update(block[len(tail):])

    return struct.pack("<IIII", *self.h)

    def hexdigest(self):
        return self.digest().hex()


if __name__ == "__main__":
    md5 = MD5()
    md5.update(input().encode())
    print(md5.hexdigest())
