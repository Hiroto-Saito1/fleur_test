# はじめに
このディレクトリでは FePO4 (w/ SOC) のWannier化を行います。

# 必要なインプット
* `inp_FePO4`
* `projgen_inp`: Wannier化の際にどの軌道に射影するかを記述します。

Feの2pをセミコアとして扱うために、 inp_FePO4 に以下を追記しました。
```
&atom element="Fe" econfig="1s2 2s2 2p6|3s2 3p6 4s2 3d6" lo="2p 3s 3p" /
```
これは、ハイフンで区切られた前の1s,2s,2pをコアとして扱い、後ろの3s,3p,4s,3dを価電子として扱うことを意味します。(コアとして扱われた軌道について、fleurはブロッホ状態を計算しません。ただしこれは擬ポテンシャル法のように「コアの電子準位を固定する」と言う意味ではありません。)

3s,3pは局在気味なので、平面波を補強するために局在基底(lo)を追加するのがfleurのデフォルトのFeの電子配置です。(`default.econfig` も参照。)

さらに今回は、loに2pを加えることで、2pのブロッホ状態を計算するように明示的に指定しています。(詳細は https://www.flapw.de/MaX-4.0/documentation/inpgen/ を参照。)


projgen_inp の中身は以下のようです。
```
Fe 0 0 -4
Fe 1 0 -3
Fe 2 0 -4
O 1 0 -3
```
3列の数字のうち、1列目は軌道量子数 l (l=0,1,2はs,p,dに対応)を意味し、
2列目は磁気量子数 m (m=0に指定すれば、px, py, pzなどの全て)を意味し、
3列目は主量子数 r で、r=0に設定すると自動で決められる。
r=1,2,3は水素の動径関数に対応し、r=-1,-2,-3はfleur内部のMT半径内の基底の動径関数に対応する。(abs(r)-1が節の数に相当。)

上記の場合、Feの3s, 2p, 3d, Oの2pの全軌道を指定しています。

(詳細は https://www.flapw.de/MaX-5.1/documentation/wannierprojgeninp/ を参照。)

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

## 射影の設定
`projgen_inp` から、fleurの計算に必要な詳細なインプットファイル `proj` を作ります。

まず、wannier計算のフラグをインプットに書き足します。inp.xml を開いて、
```
<output dos="F" band="F" slice="F">
```
の箇所を
```
<output dos="F" band="F" slice="F" wannier="T">
    <wannier>
    <bandSelection minSpinUp="1" maxSpinUp="200"/>
    <jobList> projgen stopopt </jobList>
    </wannier>
```
のように書き換えます。
`minSpinUp="1" maxSpinUp="200"` の部分は、DFTの何番目から何番目までのバンドを射影の対象に入れるかを指定します。(とりあえず、num_wann=168 より大きい値にしておきます。)

次に、fleur
```
$FLEUR_DIR/fleur_MPI
```
を実行します。`proj` が生成されます。

## nscf計算
Wannier化を行うために、一様グリッドでのエネルギー固有状態を計算します。

まず、kpts.xml に `wannier` と言う名前の、5\*3\*6の一様グリッドを作ります。
```
$FLEUR_DIR/inpgen -inp.xml -kpt wannier#gamma@grid=5,3,6 -noKsym
```
以降の計算でこのグリッドを使うように、 inp.xml も以下のように書き換えましょう。
```
<kPointListSelection listName="wannier"/>
```

次に、 inp.xml を書き換えて、`prepwan90` をオンにします。
```
<jobList> prepwan90 </jobList>
```

fleurを実行。ここが一番時間のかかる計算です。
```
mpirun -n 24 $FLEUR_DIR/fleur_MPI -eig hdf
```
これで、各k点での固有値・固有状態の書かれた `eig.hdf` が作られます。
(fleur_Max系はここの並列化がうまく行えていないようで、1週間くらいかかると思います。)

### 補足
「射影の設定」と「nscf計算」の順番は逆でも良いです。
(この後の計算で、woutのspreadが広すぎるなど、計算がうまく行っていない場合は射影の設定だけやり直せばよく、nscf計算はもう一度やる必要はありません。)

## amnとmmnの計算
まず、inp.xml を以下のように書き換えて、
```
<output dos="F" band="F" slice="F" wannier="T" eig66="T">
```
`eig66="T"` にすることで、先ほど計算した eig.hdf を使うようになります。

次に、 inp.xml を書き換えて、`matrixamn matrixmmn` をオンにします。
```
<jobList> matrixamn matrixmmn </jobList>
```

fleurを実行。
```
mpirun -n 24 $FLEUR_DIR/fleur_MPI -eig hdf
```

最終的に、`WF1.eig`, `WF1.amn`, `WF1.mmn`, `WF1.win` が出力されます。
(WF2.winなども作られますが、この場合は無視して大丈夫です。)

## Wannier化
あとは `WF1.win` を適宜編集して、
```
mpirun -n 24 $WANNIER_DIR/wannier90.x WF1
```
を実行すれば Wannier化は完了です。