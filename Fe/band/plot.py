import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from scipy.constants import physical_constants

sys.path.append("../../")
from wannier_utils.hamiltonian import HamK, HamR


class DftBand:
    """
    kptsを読み、klenを得る。
    bands.1を読む。
    """

    def __init__(self):
        with open("kpts", "r") as f:
            first_line = f.readline().strip()
            first_number_str = first_line.split()[0]
            klen = int(first_number_str)

        band = pd.read_table("bands.1", header=None, delimiter="\s+")
        self.band = self.insert_empty_rows(band, klen)

    def insert_empty_rows(self, df: pd.DataFrame, interval: int):
        """
        プロットのためにbandのDataFrameに空の行を追加する。
        """
        segments = []
        for i in range(0, len(df), interval):
            segment = df.iloc[i : i + interval]
            segments.append(segment)
            empty_row = pd.DataFrame(np.nan, index=[0], columns=df.columns)
            segments.append(empty_row)
        segments.pop()
        new_df = pd.concat(segments).reset_index(drop=True)
        return new_df


class WanBand:
    """
    kptsを読み、kpathの座標を全て得る。
    WF1_hr.datを対角化する。
    spin polarizationを計算する。
    """

    def __init__(self, ham):
        self.num_wann = ham.num_wann
        kp_list_all = self.read_kpts()
        self.band, vk_all = self.calc_band(ham, kp_list_all)
        self.spin_polarization = self.calc_spin_polarization(vk_all)

    def read_kpts(self):
        """
        kptsを読み、全てのk点の座標(coord)を入手する。
        Returns:
            Array in (3, klen).
        """
        coord = []
        with open("kpts", "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            parts = line.split()
            array = np.array([float(parts[0]), float(parts[1]), float(parts[2])])
            coord.append(array)
        return np.array(coord).T

    def calc_band(self, ham, kp_list_all):
        """
        Returns:
            ek_all: Array in (klen, num_wann).
            vk_all: Array in (klen, num_wann, num_wann). 固有ベクトルは縦ベクトル。
        """
        klen = np.shape(kp_list_all)[1]
        ek_all = np.zeros([klen, ham.num_wann])
        vk_all = np.zeros([klen, ham.num_wann, ham.num_wann], dtype=complex)
        for ik in range(klen):
            ham_k = HamK(ham, kp_list_all[:, ik], diagonalize=True)
            ek_all[ik, :] = ham_k.ek
            vk_all[ik, :, :] = ham_k.uk
        return ek_all, vk_all

    def calc_spin_polarization(self, vk_all):
        """
        バンドの各k点でのスピン分極を計算する。
        Args:
            vk_all: Array in (klen, num_wann, num_wann). 固有ベクトルは縦ベクトル。
        Returns:
            spin_polarizaiton: Array in (klen, num_wann, 3).
        """
        klen = np.shape(vk_all)[0]
        num_wann = np.shape(vk_all)[1]
        spin_polarizaiton = np.zeros([klen, num_wann, 3])
        pauli_matrix = (
            np.array([[0, 1], [1, 0]]),
            np.array([[0, -1j], [1j, 0]]),
            np.array([[1, 0], [0, -1]]),
        )
        _vk_all = vk_all.reshape([klen, 2, int(num_wann / 2), num_wann])

        spin_polarizaiton = np.einsum(
            "ijkl, mjr, irkl -> ilm", np.conjugate(_vk_all), pauli_matrix, _vk_all
        )
        return spin_polarizaiton.real


if __name__ == "__main__":
    """
    DFTとWannierを重ねてプロットする。
    """
    # Hartree to eV conversion factor
    hartree_to_ev = physical_constants["Hartree energy in eV"][0]
    E_F = 0.4123759401 * hartree_to_ev
    print(f"Fermi energy: {E_F} eV")
    tick = [0, 1.17343, 2.00317, 2.58988, 3.60610, 4.43583]
    tick = [_ / np.max(tick) for _ in tick]
    label = ["$\\Gamma$", "H", "N", "P", "$\\Gamma$", "N"]
    dft = DftBand()
    wann = WanBand(ham=HamR(hr_dat=Path("../wan/WF1_hr.dat")))

    # plotting
    plt.figure()
    plt.plot(
        dft.band.iloc[:, 0] / np.max(dft.band.iloc[:, 0]),
        dft.band.iloc[:, 1],
        color="black",
    )

    for nw in range(wann.num_wann):
        plt.scatter(
            dft.band.iloc[: len(wann.band), 0] / np.max(dft.band.iloc[:, 0]),
            wann.band[:, nw] - E_F,
            c=wann.spin_polarization[:, nw, 2],
            cmap="coolwarm",
            marker=".",
        )

    plt.colorbar(label="spin polarization $\sigma_z$")
    plt.axhline(y=5, color="grey", linestyle="--")
    plt.xticks(ticks=tick, labels=label)
    plt.ylim(-10, 10)
    plt.xlim(0, 1)
    plt.ylabel("$E - E_F$ [eV]")
    plt.grid()
    plt.savefig("band.pdf")
