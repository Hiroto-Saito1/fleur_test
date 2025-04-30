#!/bin/zsh
#PBS -q GroupA
#PBS -l nodes=1:ppn=12

source /opt/intel_2022/setvars.sh --force intel64
conda activate mae
export LD_LIBRARY_PATH=~/hdf5/hdf5-1.12.3/hdf5/lib:$LD_LIBRARY_PATH
cd $PBS_O_WORKDIR 

FLEUR_DIR=/home/hirotosaito/codes/fleur_v26_uhu/src/
WANNIER_DIR=/home/hirotosaito/codes/qe-7.2/wannier90-3.1.0/

#./clear.sh
#$FLEUR_DIR/inpgen.x < inpgen.Fe
#mpirun -n 12 $FLEUR_DIR/fleur.x 
#cp out scf.out

# dos=T, emax_dos=1, band=T
mpirun -n 12 $FLEUR_DIR/fleur.x 
cp out dos.out

rm -f submit_toki.sh.*