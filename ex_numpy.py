#!/usr/bin/env python3
import numpy as np

if __name__ == '__main__':
    np.seterr(over='ignore')
    a = np.zeros(100, dtype=np.uint8)
    a[0] = 255
    print(a[0])
    print(a[0]+1)
    print(a[1]-1)
    a[2] = 0x12
    a[3] = 0x34
    print(hex((0x12 << 8) + 0x34))
    print(hex((int(a[2]) << 8) + int(a[3])))
