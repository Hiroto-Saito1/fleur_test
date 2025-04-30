set terminal postscript enhanced color "Times-Roman" 20
set xlabel ""
set ylabel "E - E_F (eV)"
set nokey
set title "FePO4"
set arrow from  0.00000, -9.0 to  0.00000,  5.0 nohead
set arrow from  0.28619, -9.0 to  0.28619,  5.0 nohead
set arrow from  0.45516, -9.0 to  0.45516,  5.0 nohead
set arrow from  0.74135, -9.0 to  0.74135,  5.0 nohead
set arrow from  0.91032, -9.0 to  0.91032,  5.0 nohead
set arrow from  1.25841, -9.0 to  1.25841,  5.0 nohead
set arrow from  1.54460, -9.0 to  1.54460,  5.0 nohead
set arrow from  1.71357, -9.0 to  1.71357,  5.0 nohead
set arrow from  1.99976, -9.0 to  1.99976,  5.0 nohead
set arrow from  2.16873, -9.0 to  2.16873,  5.0 nohead
set arrow from  0.00000, 0.0 to  2.16873, 0.0 nohead lt 3
set xtics (" "  0.00000, \
           "X"  0.28619, \
           "S"  0.45516, \
           "Y"  0.74135, \
           " "  0.91032, \
           "Z"  1.25841, \
           "U"  1.54460, \
           "R"  1.71357, \
           "T"  1.99976, \
           "Z"  2.16873  )
set label "G" at   0.00000, -9.65 center font "Symbol,20"
set label "G" at   0.91032, -9.65 center font "Symbol,20"
set ytics -8,2,4
plot [0:  2.16874] [-9:5] \
"bands.2" using 1:($2+0.00)  w p pt 12 ps 0.5, \
"bands.1" using 1:($2+0.00)  w p pt  7 ps 0.5
