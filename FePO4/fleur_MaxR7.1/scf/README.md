# はじめに
このディレクトリでは FePO4 (w/ SOC) のscf計算を行います。

# 必要なインプット
* `inp_FePO4`

Feの2pをセミコアとして扱うために、 inp_FePO4 に以下を追記しました。
```
&atom element="Fe" econfig="1s2 2s2 2p6|3s2 3p6 4s2 3d6" lo="2p 3s 3p" /
```
これは、ハイフンで区切られた前の1s,2s,2pをコアとして扱い、後ろの3s,3p,4s,3dを価電子として扱うことを意味します。(コアとして扱われた軌道について、fleurはブロッホ状態を計算しません。ただしこれは擬ポテンシャル法のように「コアの電子準位を固定する」と言う意味ではありません。)

3s,3pは局在気味なので、平面波を補強するために局在基底(lo)を追加するのがfleurのデフォルトのFeの電子配置です。(`default.econfig` も参照。)

さらに今回は、loに2pを加えることで、2pのブロッホ状態を計算するように明示的に指定しています。(詳細は https://www.flapw.de/MaX-4.0/documentation/inpgen/ を参照。)


`./clear.sh` で必要なインプット以外のファイルを消し、計算を初期化できます。

# 計算手順
詳細は `submit_toki.sh` を参照。

## インプットファイルの作成
`inp_FePO4` から、fleurの計算に必要な詳細なインプットファイル `inp.xml` を作ります。
```
$FLEUR_DIR/inpgen -f inp_FePO4
```
inp.xml の各パラメーターの詳細は、
https://www.flapw.de/MaX-5.0/documentation/fleurInputFile/
を見てください。

例えば、inp.xml を開くと `jspins=2` となっているのがわかります。
これはFeのような磁性元素の場合、デフォルトで磁性あり(ただしコリニア)で計算するためです。
また `l_soc=T` となっているのはinp_FePO4でSOCを指定したことに対応しています。
(fleurでSOCはscf計算収束後の電荷密度にのみ入れられます。QEでnscfから後入れした場合に相当。)


## scf計算
まず、イタレーション数をデフォルトの15から100に増やします。
inp.xml を開いて、`itmax="100"` と書き換えましょう。
次に、
```
mpirun -n 24 $FLEUR_DIR/fleur.x 
```
を行うとscf計算が開始され、 電子密度 `cdn.hdf` が返されます。

収束性は以下のように確認できます。
```
cat out |grep dist

No new postions, force convergence required= 0.00001; max force distance= 1.50119
---->    distance of charge densities for spin  1                 it=    1:    17.915617 me/bohr**3
---->    distance of charge densities for spin  2                 it=    1:    25.775814 me/bohr**3
---->    distance of charge densities for it=    1:    26.667848 me/bohr**3
---->    distance of spin densities for it=    1:    35.490136 me/bohr**3
No new postions, force convergence required= 0.00001; max force distance= 0.06732
---->    distance of charge densities for spin  1                 it=    2:    17.260171 me/bohr**3
---->    distance of charge densities for spin  2                 it=    2:    23.184496 me/bohr**3
---->    distance of charge densities for it=    2:    22.887887 me/bohr**3
---->    distance of spin densities for it=    2:    33.867585 me/bohr**3
No new postions, force convergence required= 0.00001; max force distance= 0.46023
---->    distance of charge densities for spin  1                 it=    3:    15.941231 me/bohr**3
---->    distance of charge densities for spin  2                 it=    3:    36.189171 me/bohr**3
---->    distance of charge densities for it=    3:    50.708613 me/bohr**3
---->    distance of spin densities for it=    3:    23.583773 me/bohr**3
```

計算が終わると、標準出力に収束性はまとめられます。
```
Iteration:           1  Distance:   35.4885305104185     
 Iteration:           2  Distance:   33.8653376494640     
 Iteration:           3  Distance:   50.7404558203077     
 Iteration:           4  Distance:   27.7908146058647     
 Iteration:           5  Distance:   19.8301168358131     
 Iteration:           6  Distance:   18.5166332277723     
 Iteration:           7  Distance:   12.5522735237637     
 Iteration:           8  Distance:   12.2405434607675     
 Iteration:           9  Distance:   10.1159574218830     
 Iteration:          10  Distance:   9.15730411237873     
 Iteration:          11  Distance:   8.03413211505450     
 Iteration:          12  Distance:   7.18294215712047     
 Iteration:          13  Distance:   4.08109423033364     
 Iteration:          14  Distance:   1.65351339886313     
 Iteration:          15  Distance:  0.875669788277697     
 Iteration:          16  Distance:  0.848142216789317     
 Iteration:          17  Distance:  0.588843562619768     
 Iteration:          18  Distance:  0.110453887902152     
 Iteration:          19  Distance:  0.125349259707718     
 Iteration:          20  Distance:  5.418705525283948E-002
 Iteration:          21  Distance:  3.629878203824678E-002
 Iteration:          22  Distance:  3.202231617438386E-002
 Iteration:          23  Distance:  5.285673279060724E-003
 Iteration:          24  Distance:  2.317735374176168E-003
 Iteration:          25  Distance:  1.496028938303637E-003
 Iteration:          26  Distance:  9.275392510444048E-004
 Iteration:          27  Distance:  3.100561493627207E-004
 Iteration:          28  Distance:  1.244202358724453E-004
 Iteration:          29  Distance:  1.468811209015877E-004
 Iteration:          30  Distance:  1.062583363824277E-004
 Iteration:          31  Distance:  6.705799928425307E-005
 Iteration:          32  Distance:  3.080717928122884E-005
 Iteration:          33  Distance:  1.244324177138289E-005
 Iteration:          34  Distance:  4.994094315245351E-006
```
この場合は、34イタレーションで1e-5以下に電子密度が収束したことがわかります。
