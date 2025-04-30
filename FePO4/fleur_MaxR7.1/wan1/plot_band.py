import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

sys.path.append("/home/hirotosaito/github_projects/ishiwata_lab/src")
from wannier_utils.hamiltonian import HamK, HamR


class DftBand:
    """
    kpts.xmlを読み、klen, high-sym k点の名前, 位置を得る。
    bands.1を読む。
    """

    def __init__(
        self, bands_path: Path = Path("bands.1"), kpts_path: Path = Path("kpts.xml")
    ):
        klen, self.label, self.index = self.read_kpts_xml(kpts_path, name="path-2")

        band = pd.read_table(bands_path, header=None, delimiter="\\s+")
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

    def read_kpts_xml(self, kpts_path, name="path-2"):
        """
        kpts.xmlを読み、klen, high-sym k点の名前, 位置を得る。
        """
        tree = ET.parse(kpts_path)
        root = tree.getroot()
        label = []
        index = []
        for _kpointlist in root.iter("kPointList"):
            if _kpointlist.get("name") == name:
                klen = int(_kpointlist.get("count"))
                for _index, _kpoint in enumerate(_kpointlist.iter("kPoint")):
                    _label = _kpoint.get("label")
                    if _label is not None:
                        label.append(str(_label))
                        index.append(int(_index))
        label = ["$\\Gamma$" if _ == "g" else _ for _ in label]
        return klen, label, index


class WanBand:
    """
    kpts.xmlを読み、kpathの座標を全て得る。
    WF1_hr.datを対角化する。
    """

    def __init__(self, ham: HamR, kpts_path: Path = Path("kpts.xml")):
        self.num_wann = ham.num_wann
        kp_list_all = self.read_kpts_xml(kpts_path)
        self.band, vk_all = self.calc_band(ham, kp_list_all)

    def read_kpts_xml(self, kpts_path):
        """
        kpts.xmlを読み、path-2の全てのk点の座標(coord)を入手する。
        Returns:
            Array in (3, klen).
        """
        tree = ET.parse(kpts_path)
        root = tree.getroot()
        coord = []
        for _kpointlist in root.iter("kPointList"):
            if _kpointlist.get("name") == "path-2":
                for _kpoint in _kpointlist.iter("kPoint"):
                    coord.append(_kpoint.text.strip())
        coord = [np.array(list(map(float, _.split()))) for _ in coord]
        return coord

    def calc_band(self, ham, kp_list_all):
        """
        Returns:
            ek_all: Array in (klen, num_wann).
            vk_all: Array in (klen, num_wann, num_wann). 固有ベクトルは縦ベクトル。
        """
        ek_all = np.zeros([len(kp_list_all), ham.num_wann])
        vk_all = np.zeros([len(kp_list_all), ham.num_wann, ham.num_wann], dtype=complex)
        for ik, k in enumerate(kp_list_all):
            ham_k = HamK(ham, k, diagonalize=True)
            ek_all[ik, :] = ham_k.ek
            vk_all[ik, :, :] = ham_k.uk
        return ek_all, vk_all


if __name__ == "__main__":
    """
    DFTとWannierを重ねてプロットする。
    """
    ham = HamR(tb_dat=Path("WF1_tb.dat"))
    dft = DftBand(
        bands_path=Path("../band/bands.1"), kpts_path=Path("../band/kpts.xml")
    )
    wan = WanBand(ham, kpts_path=Path("../band/kpts.xml"))

    # plotting
    plt.rcParams["font.size"] = 16
    plt.rcParams["figure.subplot.left"] = 0.20
    plt.rcParams["figure.subplot.bottom"] = 0.20
    plt.figure()

    # DFT
    plt.plot(
        dft.band.iloc[:, 0],
        dft.band.iloc[:, 1],
        color="black",
    )

    '''
    # Wannier
    for nw in range(ham.num_wann):
        plt.plot(dft.band.iloc[:240, 0], wan.band[:, nw], color="red", linestyle="--")
    '''

    plt.xticks(ticks=[dft.band.iloc[i, 0] for i in dft.index], labels=dft.label)
    plt.xlim(np.min(dft.band.iloc[:, 0]), np.max(dft.band.iloc[:, 0]))
    plt.ylabel("$E - E_F$ [eV]")
    plt.grid()
    plt.ylim(-70, 16)
    plt.savefig("band.pdf")
    plt.ylim(-12, 4)
    plt.savefig("band_detail.pdf")
