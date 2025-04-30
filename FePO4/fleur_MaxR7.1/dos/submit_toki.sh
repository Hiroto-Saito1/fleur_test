#!/bin/zsh
#PBS -q GroupD
#PBS -l nodes=1:ppn=32

source /opt/intel_2022/setvars.sh --force intel64
source /home/hirotosaito/.bashrc
conda activate mae
cd $PBS_O_WORKDIR 
rm -f submit_toki.sh.*

FLEUR_DIR=/home/hirotosaito/codes/fleur_MaxR7.1/build
WANNIER_DIR=/home/hirotosaito/codes/fleur_MaxR7.1/external/wannier90
SRC_DIR=/home/hirotosaito/github_projects/ishiwata_lab/src

#./clear.sh

## dos計算
## inp.xml を開いて、dos="T" に書き換え
## inp.xml を開いて、minEnergy="-2.50000000*Htr" maxEnergy="2.50000000*Htr" に書き換え
mpirun -n 32 $FLEUR_DIR/fleur_MPI

