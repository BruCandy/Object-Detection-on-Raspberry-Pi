# Object-Detection-on-Raspberry-Pi

## 解説

Raspberry Pi 4Bを使用して、お気に入りのグミ（ツブグミ、カムカムレモン）を検出し、LCDモニターに検出したグミの名前を表示した。

## 結果

左側のスイッチで初期化をし、右側のスイッチで画像を撮る。Loadingの最中はLEDが点灯するようにした。

<p align="center">
  <img src="docs/images/figure1.jpg" alt="No　date" width="300" height="300">
</p>

検出器は以下のように使用した。白い台上にグミを置き、上からwebカメラで画像を撮った。

<p align="center">
  <img src="docs/images/figure6.png" alt="No　date" width="300" height="300">
</p>

検出結果は以下の通り。

左上：二つ以上検出した場合

右上：何も検出しなかった場合

左下：ツブグミを検出した場合

右下：カムカムレモンを検出した場合

<p align="center">
  <img src="docs/images/figure2.jpg" alt="No　date" width="300" height="300">
  <img src="docs/images/figure3.jpg" alt="No　date" width="300" height="300">
</p>
<p align="center">
  <img src="docs/images/figure4.jpg" alt="No　date" width="300" height="300">
  <img src="docs/images/figure5.jpg" alt="No　date" width="300" height="300">
</p>
