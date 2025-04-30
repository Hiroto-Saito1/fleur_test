"""
kpointgen.f に対応するpythonプログラム。
Default: 4*4*4

Example:
    >>> python kpointgen.py 5 5 5
"""

import sys


def findkgt(nu):
    nnu = nu
    if nnu == 0:
        raise ValueError("nnu == 0")
    for _ in range(3):
        if nnu == 1:
            break
        if nnu % 5 != 0:
            break
        nnu //= 5
    for _ in range(3):
        if nnu == 1:
            break
        if nnu % 2 != 0:
            break
        nnu //= 2
    return nnu


def generate_kpoints(dim, l_shift, Nx=4, Ny=4, Nz=4):
    num = Nx * Ny * Nz
    nnx = findkgt(Nx)
    nny = findkgt(Ny)
    nnz = findkgt(Nz)
    scale = nnx
    if nny != nnx:
        scale *= nny
    if nnz != nny and nnz != nnx:
        scale *= nnz

    ilen1 = 1.0 / Nx
    ilen2 = 1.0 / Ny
    ilen3 = 1.0 / Nz
    limit1 = Nx - 1
    limit2 = Ny - 1
    limit3 = Nz - 1

    shift1, shift2, shift3 = 0.0, 0.0, 0.0
    if l_shift:
        shift1 = limit1 * ilen1 / 2.0
        shift2 = limit2 * ilen2 / 2.0
        shift3 = limit3 * ilen3 / 2.0

    kpoints = []
    if dim != 2:
        for c1 in range(limit1 + 1):
            for c2 in range(limit2 + 1):
                for c3 in range(limit3 + 1):
                    i1 = (ilen1 * c1 - shift1) * scale
                    i2 = (ilen2 * c2 - shift2) * scale
                    i3 = (ilen3 * c3 - shift3) * scale
                    kpoints.append([i1, i2, i3, 1.0])
    else:
        for c1 in range(limit1 + 1):
            for c2 in range(limit2 + 1):
                i1 = (ilen1 * c1 - shift1) * scale
                i2 = (ilen2 * c2 - shift2) * scale
                kpoints.append([i1, i2, 1.0])

    return num, scale, kpoints


if __name__ == "__main__":
    dim = 3  # int(input("Specify dimension [1, 2, or 3]: "))
    l_shift = False  # input("Symmetric to origin? [T or F]: ").strip().upper() == 'T'
    Nx, Ny, Nz = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

    """
    if dim == 3:
        print("Creates three-dimensional k-point set.")
        Nz = int(input("Nz= "))
        Ny = int(input("Ny= "))
        Nx = int(input("Nx= "))
    elif dim == 2:
        print("Create two-dimensional k-point set.")
        Ny = int(input("Ny= "))
        Nx = int(input("Nx= "))
    elif dim == 1:
        print("Create one-dimensional k-point set.")
        Nx = int(input("Nx= "))
    else:
        raise ValueError('Unknown dimension')
    """

    num, scale, kpoints = generate_kpoints(dim, l_shift, Nx, Ny, Nz)
    print(f"Number of k-points: {num}")
    print(f"scale= {scale}")

    with open("kpts", "w") as f:
        if dim != 2:
            f.write(f"{num:5d}{scale:20.10f}\n")
            for kp in kpoints:
                f.write(f"{kp[0]:10.5f}{kp[1]:10.5f}{kp[2]:10.5f}{kp[3]:10.5f}\n")
        else:
            f.write(f"   {num}        {scale:.10f}   F\n")
            for kp in kpoints:
                f.write(f"{kp[0]:10.5f}   {kp[1]:10.5f}   {kp[2]:10.5f}\n")
