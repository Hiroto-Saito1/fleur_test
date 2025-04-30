# はじめに
tokiでコンパイル済みの fleur_v26 を使います。
(/home/hirotosaito/codes/fleur_v26_uhu/src/fleur_v26_uhu)

古いバージョンですが、新しいバージョン (fleur_MaxR系) より早いです。

もしコンパイルしたい場合は、上記のディレクトリを好きな場所にコピーして、 `make` してください。
(Makefileを見ていただくとわかるのですがhdf5-1.12.3が必要なので、mpiifortでhdf5-1.12.3をコンパイルしてからMakefile内のパスを適宜書き換えて、makeしてください。)

# ディレクトリの内容
* Fe: bcc Fe (w/ SOC)　の例。
* utils: 計算のインプットファイルを作るためのpythonプログラム。