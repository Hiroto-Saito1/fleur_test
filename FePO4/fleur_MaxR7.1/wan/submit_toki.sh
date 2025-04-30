#!/bin/zsh
#PBS -q GroupC
#PBS -l nodes=1:ppn=16

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
#mpirun -n 32 $FLEUR_DIR/fleur_MPI

## 射影の設定
## <output dos="F" band="F" slice="F" wannier="T">
## <wannier>
## <bandSelection minSpinUp="1" maxSpinUp="200"/>
## <jobList> projgen stopopt </jobList>
## </wannier>
#$FLEUR_DIR/fleur_MPI

## nscf計算
## 一様 kgridを作る
#$FLEUR_DIR/inpgen -inp.xml -kpt wannier#gamma@grid=5,3,6 -noKsym
## inp.xml を開いて、<kPointListSelection listName="wannier"/> に書き換え
## inp.xml を開いて、<jobList> prepwan90 </jobList> に書き換え
#mpirun -n 32 $FLEUR_DIR/fleur_MPI -eig hdf

## amnとmmnの計算
## inp.xml を開いて、<output dos="F" band="F" slice="F" wannier="T" eig66="T"> に書き換え
## inp.xml を開いて、<jobList> matrixamn matrixmmn </jobList> に書き換え
#mpirun -n 16 $FLEUR_DIR/fleur_MPI -eig hdf

## Wannier化
## WF1.win を適宜編集
mpirun -n 16 $WANNIER_DIR/wannier90.x WF1
