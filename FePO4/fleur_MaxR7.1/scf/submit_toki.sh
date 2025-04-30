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

## インプットファイルの作成
#$FLEUR_DIR/inpgen -f inp_FePO4

## scf計算
## inp.xml を開いて、itmax="100" と書き換えます
mpirun -n 32 $FLEUR_DIR/fleur_MPI

