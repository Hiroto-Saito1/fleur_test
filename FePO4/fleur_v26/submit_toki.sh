#!/bin/zsh
#PBS -q GroupD
#PBS -l nodes=1:ppn=16

source /opt/intel_2022/setvars.sh --force intel64
source /home/hirotosaito/.bashrc
conda activate mae
export LD_LIBRARY_PATH=~/hdf5/hdf5-1.12.3/hdf5/lib:$LD_LIBRARY_PATH
cd $PBS_O_WORKDIR 

FLEUR_DIR=/home/hirotosaito/codes/fleur_v26_uhu/src/fleur_v26_uhu/
WANNIER_DIR=/home/hirotosaito/codes/qe-7.2/wannier90-3.1.0/
UTILS_DIR=/home2/hirotosaito/to_terao/utils/

rm -f submit_toki.sh.*

## インプットファイルの作成
#$FLEUR_DIR/inpgen.x < inp_FePO4 

## scf計算
mpirun -n 16 $FLEUR_DIR/fleur.x 

## 射影の設定1
#python $UTILS_DIR/rewrite_wann_inp.py --projgen --byindex1=0 --byindex2=80
## 射影の設定2
#$FLEUR_DIR/fleur.x

## nscf計算
#python $UTILS_DIR/kpointgen.py 6 6 6
#python $UTILS_DIR/rewrite_wann_inp.py --prepwan90 --byindex1=0 --byindex2=80
#$FLEUR_DIR/fleur.x 

## amnとmmnの計算
#python $UTILS_DIR/rewrite_wann_inp.py --amn_mmn --byindex1=0 --byindex2=80
#$FLEUR_DIR/fleur.x 

## Wannier化
# mpirun -n 32 $WANNIER_DIR/wannier90.x WF1

