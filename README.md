# dend-cs-rs-editor

## 概要

dend-cs-rs-editor は、電車でD ClimaxStage, RisingStage の競技列車のパラメータを、GUI画面上で編集するソフトウェアである。

## 動作環境

* 電車でDが動くコンピュータであること
* OS: Windows 10 64bit の最新のアップデートであること
* OSの端末が日本語に対応していること

※ MacOS 、 Linux などの Unix 系 OS での動作は保証できない。


## 免責事項

このプログラムを使用して発生したいかなる損害も製作者は責任を負わない。

このプログラムを実行する前に、自身のコンピュータのフルバックアップを取得して、
安全を担保したうえで実行すること。
このプログラムについて、電車でD 作者である、地主一派へ問い合わせてはいけない。

このソフトウェアの更新やバグ取りは、作者の義務ではなく解消努力目標とする。
Issue に上げられたバグ情報が必ず修正されるものではない。

* ライセンス：MIT

電車でD の正式なライセンスを持っていること。

本プログラムに関連して訴訟の必要が生じた場合、東京地方裁判所を第一審の専属的合意管轄裁判所とする。

このプログラムのバイナリを実行した時点で、この規約に同意したものと見なす。

## 実行方法

![title](https://github.com/khttemp/dend-cs-rs-editor/blob/main/image/title.png)

1. ラジオボタンで、ゲームを選ぶ。初期状態は「Rising Stage」になっている。

2. メニュの「ファイルの開く」でBINファイルを開く。

    Climax Stageは「TRAIN_DATA3RD.BIN」、Rising Stageは「TRAIN_DATA4TH.BIN」を開く。

    必ず、プログラムが書込みできる場所で行ってください

3. リストにある車両を選ぶ

4. 「この車両を修正する」ボタンで、速度や性能の修正ボタンが活性化されます。修正している間には、車両を選ぶことができません

5. 「保存する」ボタンで、修正した性能を保存できます。

## ソースコード版の実行方法

このソフトウェアは Python3 系で開発されているため、 Python3 系がインストールされた開発機であれば、
ソースコードからソフトウェアの実行が可能である。


### 依存ライブラリ

* Tkinter

  Windows 版 Python3 系であれば、インストール時のオプション画面で tcl/tk and IDLE のチェックがあったと思う。
  tcl/tk and IDLE にチェックが入っていればインストールされる。
  
  Linux 系 OS では、 パッケージ管理システムを使用してインストールする。

### 動作環境

以下の環境で、ソースコード版の動作確認を行った

* OS: Windows 10 64bit
* Python 3.8.8 64bit
* pip 20.2.3 64bit

### ソースコードの直接実行

Windows であれば以下のコマンドを入力する。


````
> python editor.py
````

これで、実行方法に記載した画面が現れれば動作している。


### FAQ

* Q. ImportError: No module named tkinter と言われて起動しない

  * A. 下のようなメッセージだろうか？ それであれば、 tkinter がインストールされていないので、インストールすること。
  
  ````
  > python editor.py
  Traceback (most recent call last):
    File "editor.py", line 6, in <module>
      from tkinter import *
  ImportError: No module named tkinter
  ````


* Q. 電車でD ClimaxStage なのに、 TRAIN_DATA3RD.BIN が無い。

  または、電車でD RisingStage なのに、TRAIN_DATA4TH.BIN がない。  
  
  * A. Climax StageはPatch004.Pack、Rising StageはPatch_4th_4を

    GARbro のような、アーカイバで展開すると得られる。
  * A. GARbro を使用して空パスワードで解凍すると無効なファイルになるので、適切なパスワードを入力すること。


* Q. BINファイルを指定しても、「電車でDのファイルではない、またはファイルが壊れた可能性があります。」と言われる

  * A. 抽出方法が間違っているか、抽出時のパスワードが間違っているのでは？作業工程をやり直した方がよい。

* Q. BINファイルを改造しても、変化がないけど？

  * A. 既存のPackファイルとフォルダーが同時にあるなら、Packファイルを優先して読み込んでいる可能性がある。

    読み込みしないように、抽出したPackファイルを変更するか消そう。

* Q. ダウンロードがブロックされる、実行がブロックされる、セキュリティソフトに削除される

  * A. ソフトウェア署名などを行っていないので、ブラウザによってはダウンロードがブロックされる
  * A. 同様の理由でセキュリティソフトが実行を拒否することもある。



### Windows 版実行バイナリ（ .exeファイル ）の作成方法

pyinstaller か py2exe ライブラリをインストールする。 pip でも  easy_install  でも構わない。

下は、 pyinstaller を使用して、Windows 版実行バイナリ（ .exeファイル ）を作る例である。

````
> pyinstaller editor.py --onefile
（ コンソール出力は省略 ）
````

dist フォルダーが作られて、 editor.exe が出力される。


以上。