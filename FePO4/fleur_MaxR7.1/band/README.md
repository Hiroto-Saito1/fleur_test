# はじめに
このディレクトリでは FePO4 (w/ SOC) のバンド計算を行います。
scf計算までは `../scf` をもとに先に行ってください。

# 計算手順
詳細は `submit_toki.sh` を参照。

## band計算
inp.xml のうち、バンド計算をtrueにし、kpathを指定する。
kpathは、kpts.xmlに書かれているものを使用。
以下の部分を書き換える。

```
<output dos="F" band="T" slice="F">
```
```
<kPointListSelection listName="path-2"/>
```

また、デフォルトだとバンドを描くエネルギー領域が狭すぎるので、広げておくとよし。
```
<bandDOS minEnergy="-1.50000000*Htr" maxEnergy="1.50000000*Htr" sigma=".01500000" storeEVData="T"/>
```

あとはfleurを実行するだけ
```
mpirun -n 32 $FLEUR_DIR/fleur_MPI
```