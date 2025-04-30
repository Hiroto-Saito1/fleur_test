# はじめに
このディレクトリでは FePO4 (w/ SOC) の状態密度計算を行います。
scf計算までは `../scf` をもとに先に行ってください。


# 計算手順
詳細は `submit_toki.sh` を参照。

## dos計算
inp.xml のうち、dos計算をtrueにする。
以下の部分を書き換える。

```
<output dos="T" band="F" slice="F">
```

また、デフォルトだとdosを描くエネルギー領域が狭すぎるので、広げておくとよし。
```
<bandDOS minEnergy="-2.50000000*Htr" maxEnergy="2.50000000*Htr" sigma=".01500000" storeEVData="T"/>
```

あとはfleurを実行するだけ
```
mpirun -n 32 $FLEUR_DIR/fleur_MPI
```