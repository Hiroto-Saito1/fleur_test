set terminal postscript enhanced "Times-Roman" 20
set xlabel ""
set ylabel "E - E_F (eV)"
set nokey
set title "bcc Fe                                                                          "
set arrow from  0.00000, -9.0 to  0.00000,  5.0 nohead
set arrow from  1.17343, -9.0 to  1.17343,  5.0 nohead
set arrow from  2.00317, -9.0 to  2.00317,  5.0 nohead
set arrow from  2.58988, -9.0 to  2.58988,  5.0 nohead
set arrow from  3.60610, -9.0 to  3.60610,  5.0 nohead
set arrow from  4.43583, -9.0 to  4.43583,  5.0 nohead
set arrow from  0.00000, 0.0 to  4.43583, 0.0 nohead lt 3
set xtics (" "  0.00000, \
           "H"  1.17343, \
           "N"  2.00317, \
           "P"  2.58988, \
           " "  3.60610, \
           "N"  4.43583  )
set label "G" at   0.00000, -9.65 center font "Symbol,20"
set label "G" at   3.60610, -9.65 center font "Symbol,20"
set ytics -8,2,4
plot [0:  4.43584] [-9:5] \
"bands.2" using 1:($2+0.00)  w p pt 12 ps 0.5, \
"bands.1" using 1:($2+0.00)  w p pt  7 ps 0.5
