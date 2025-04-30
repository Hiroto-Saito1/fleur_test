# はじめに
このディレクトリでは強磁性 bcc Fe (w/ SOC) のWannier化を行います。

# 必要なインプット
* `Fe_mp-13_computed.cif`: 結晶構造。
* `projgen_inp`: Wannier化の際にどの軌道に射影するかを記述します。

projgen_inp の中身は以下のようです。
```
Fe 0 0 -4
Fe 1 0 -3
Fe 2 0 -4
```
3列の数字のうち、1列目は軌道量子数 l (l=0,1,2はs,p,dに対応)を意味し、
2列目は磁気量子数 m (m=0に指定すれば、px, py, pzなどの全て)を意味し、
3列目は主量子数 r で、r=0に設定すると自動で決められる。
r=1,2,3は水素の動径関数に対応し、r=-1,-2,-3はfleur内部のMT半径内の基底の動径関数に対応する。abs(r)-1が節の数に相当。

上記の場合、Feの3s, 2p, 3dを指定しているはずです。

(詳細は https://www.flapw.de/MaX-5.1/documentation/wannierprojgeninp/ を参照。)

`./clear.sh` で必要なインプット以外のファイルを消し、計算を初期化できます。

# 計算手順
詳細は `submit_toki.sh` を参照。

## インプットファイルの作成1
`cif` から `inp_Fe` を作ります。
```
python $UTILS_DIR/cif2inp_ase.py Fe_mp-13_computed.cif
```
SOCを入れた計算を行いたい場合、inp_Feの最後に手で以下を追記します。
```
&soc 0.0 0.0 / 
```
0.0 0.0は、SOCを入れるためのスピン量子化軸のthetaとphiを表しています。

k点数も指定したい場合には、同様にinp_Feの最後に手で以下を追記します。
```
&kpt div1=16 div2=16 div3=16 /
```

## インプットファイルの作成2
`inp_Fe` から、fleurの計算に必要な詳細なインプットファイル `inp` を作ります。
```
$FLEUR_DIR/inpgen.x < inp_Fe
```
inpの各パラメーターの詳細は、
https://www.flapw.de/Fleur-v26/v26/inpfile/
を見てください。(`fleurv26 inp` でググると出てきます。)

例えば、inpを開くと `jspins=2` となっているのがわかります。
これはFeのような磁性元素の場合、デフォルトで磁性あり(ただしコリニア)で計算するためです。
また `l_soc=T` となっているのはinp_FeでSOCを指定したことに対応しています。
(fleurでSOCは収束後の電荷密度にのみ入れられます。)

## scf計算
まず最初に
```
mpirun -n 32 $FLEUR_DIR/fleur.x 
```
を行うと `inp` を元に初期電荷密度 `cdn1` を生成します。
そのほかで重要なファイルは、k点のリストである `kpts` や、系の対称性を記入した `sym.out` です。

これらのファイルがある状態でもう一度
```
mpirun -n 32 $FLEUR_DIR/fleur.x 
```
を行うとscf計算が開始され、 固有値`eig.hdf` や固有状態 `eig01` ~ `eig09` が返されます。

収束性は以下のように確認できます。
```
cat out |grep dist
----> distance of charge densities for spin  1        it=  1:   6.373669 me/bohr**3
----> distance of charge densities for spin  2        it=  1:  11.196878 me/bohr**3
----> distance of charge densities for it=  1:  13.340351 me/bohr**3
----> distance of spin densities for it=  1:  12.410580 me/bohr**3
----> distance of charge densities for spin  1        it=  2:   5.036710 me/bohr**3
----> distance of charge densities for spin  2        it=  2:  10.247138 me/bohr**3
----> distance of charge densities for it=  2:  10.783718 me/bohr**3
----> distance of spin densities for it=  2:  12.018984 me/bohr**3
----> distance of charge densities for spin  1        it=  3:   4.504052 me/bohr**3
----> distance of charge densities for spin  2        it=  3:   6.663028 me/bohr**3
----> distance of charge densities for it=  3:   3.550113 me/bohr**3
----> distance of spin densities for it=  3:  10.805626 me/bohr**3
```
デフォルトでは9イタレーションで止まります。
(イタレーション数は `inp` 内の `itmax= 9` でいじれるのですが、バグが残っているのか9以上に増やせないです。もっと収束させたい場合には、何度も `mpirun -n 32 $FLEUR_DIR/fleur.x` を行なってください。)

## 射影の設定1
Wannier化の際にどの手順を行うかを指定する `wann_inp` ファイルを作成します。
```
python $UTILS_DIR/rewrite_wann_inp.py --projgen --byindex1=0 --byindex2=80
```
上記を実行すると `wann_inp` が作成されます。次のステップである `projgen` のみがコメントアウトされていないことがわかります。 `byindex` はそれぞれ「何番目のバンドから何番目のバンドまでを考慮するか」を指定します。

## 射影の設定2
`projgen_inp` から、fleurの計算に必要な詳細なインプットファイル `proj` を作ります。
```
$FLEUR_DIR/fleur.x
```
(mpirunだと何故かうまくいかない。)

## nscf計算
Wannier化を行うために、一様グリッドでのエネルギー固有状態を計算します。
`kpts` を書き換えて、6\*6\*6の一様グリッドを作ります。
```
python $UTILS_DIR/kpointgen.py 6 6 6
```
`wann_inp` を書き換えて、`prepwan90` をオンにします。
```
python $UTILS_DIR/rewrite_wann_inp.py --prepwan90 --byindex1=0 --byindex2=80
```
fleurを実行。ここが一番時間のかかる計算です。
```
$FLEUR_DIR/fleur.x 
```
(mpirunだと何故かうまくいかないが、並列化はできているっぽい。)

「どのk点がどのk点の隣か」を記述した `bkpts` が作られます。

## amnとmmnの計算
`wann_inp` を書き換えて、
```
python $UTILS_DIR/rewrite_wann_inp.py --amn_mmn --byindex1=0 --byindex2=80
```
fleurを実行。
```
$FLEUR_DIR/fleur.x 
```
(mpirunだと何故かうまくいかない。)

最終的に、`WF1.eig`, `WF1.amn`, `WF1.mmn`, `WF1.win` が出力されます。
(WF2.winなども作られますが、この場合は無視して大丈夫です。)

## Wannier化
あとは `WF1.win` を適宜編集して、
```
mpirun -n 32 $WANNIER_DIR/wannier90.x WF1
```
を実行。