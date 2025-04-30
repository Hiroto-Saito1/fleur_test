"""
Wannier化に必要なwann_inpの書き換えを行う。

Usage:
    rewrite_wann_inp.py (-h | --help)
    rewrite_wann_inp.py --projgen [--byindex1=<byindex1>] [--byindex2=<byindex2>]
    rewrite_wann_inp.py --prepwan90 [--byindex1=<byindex1>] [--byindex2=<byindex2>]
    rewrite_wann_inp.py --amn_mmn [--byindex1=<byindex1>] [--byindex2=<byindex2>]

Options:
  -h --help    Show this screen.
  --kpoint     rewrite kpoint.
  --projgen    make proj.
  --prepwan90  switch to prepwan90.
  --amn_mmn    switch to amn and mmn.
  --byindex1=<byindex1>  Set the first index for byindex [default: 1].
  --byindex2=<byindex2>  Set the second index for byindex [default: 24].
"""

import xml.etree.ElementTree as ET
from docopt import docopt


class RewriteWannInp:
    def __init__(self, byindex1=1, byindex2=24):
        """
        wann_inpの雛形を書き出す。
        """
        text = f"""byindex {byindex1} {byindex2}
wan90version 2.0
!projgen
!prepwan90
!matrixmmn
!matrixamn
!mmn0
!anglmom
!anglmomrs
!updown
!socmat
!socmatrs
!pauli
endjobs
"""
        with open("wann_inp", "w") as file:
            file.write(text)

    def projgen(self):
        """
        wann_inpにprojgenを加える。
        """
        with open("wann_inp", "r") as file:
            lines = file.readlines()
        updated_lines = [line.replace("!projgen", "projgen") for line in lines]
        with open("wann_inp", "w") as file:
            file.writelines(updated_lines)

    def prepwan90(self):
        """
        wann_inpにprepwan90を加える。
        """
        with open("wann_inp", "r") as file:
            lines = file.readlines()
        updated_lines = [line.replace("!prepwan90", "prepwan90") for line in lines]
        with open("wann_inp", "w") as file:
            file.writelines(updated_lines)

    def amn_mmn(self):
        """
        wann_inpにmatrixmmnとmatrixamnを加える。
        """
        with open("wann_inp", "r") as file:
            lines = file.readlines()
        updated_lines = [line.replace("!matrixmmn", "matrixmmn") for line in lines]
        updated_lines = [line.replace("!matrixamn", "matrixamn") for line in updated_lines]
        with open("wann_inp", "w") as file:
            file.writelines(updated_lines)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    byindex1 = int(arguments["--byindex1"])
    byindex2 = int(arguments["--byindex2"])

    _ = RewriteWannInp(byindex1, byindex2)
    if arguments["--projgen"]:
        _.projgen()
    if arguments["--prepwan90"]:
        _.prepwan90()
    if arguments["--amn_mmn"]:
        _.amn_mmn()
