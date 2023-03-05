# dend-lbcr-editor

## 概要

dend-lbcr-editor は、電車でD LightningStage、BurningStage、ClimaxStage、RisingStage の競技列車のパラメータを、GUI画面上で編集するソフトウェアである。

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

![title](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/title.png)

1. ラジオボタンで、ゲームを選ぶ。初期状態は「Rising Stage」になっている。

2. メニュの「ファイルの開く」でBINファイルを開く。

    Lightning Stageは「TRAIN_DATA.BIN」

    Burning Stageは「TRAIN_DATA2ND.BIN」

    Climax Stageは「TRAIN_DATA3RD.BIN」

    Rising Stageは「TRAIN_DATA4TH.BIN」を開く。

    必ず、プログラムが書込みできる場所で行ってください

3. リストにある車両を選ぶ

4. 改造したい項目を選ぶ。「速度・性能情報」、「数・モデル情報」、「レンズフレア」から選べる

## ステージ情報変更方法

※上記の機能は、Burning Stage、Climax Stage、Rising Stageのみできます。

![stage](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/stage.png)

1. ステージを選んだとき、デフォルトで適用する車両を変更できる。

2. Climax Stage以降は、台車も設定できる。

3. OKをクリックすると、すぐ保存される。

## 速度・性能変更方法

![title](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/title.png)

1. 「車両の性能をデフォルトに戻す」ボタンで、速度、または性能を全部デフォルト数値に戻すことができる。

2. 「車両情報をCSVで取り出す」ボタンで、車両情報をCSV出力する。

    一部、else以外の情報を全て取り出せる。

3. 「車両情報をCSVで上書きする」ボタンで、車両情報を改造できる。

    一部、else以外の情報を全て上書きして改造できる。

4. 「この車両を修正する」ボタンで、速度や性能の修正ボタンが活性化される。

    修正している間には、車両を選ぶことができない。

5. 「保存する」ボタンで、修正した速度や性能を保存できる。

6. 「同じ倍率で全部修正する」ボタンで、性能のある数値を

    x倍、またはx値で全車両修正できる。

7. 数値を改造した場合、デフォルトより高いと赤色に、低いと青色になる。

## 数・モデル情報変更方法

![model](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/model.png)

1. 車両の枠は編成やカラーの数、各編成に適用するモデル、パンタ、COLを設定できる。

2. ノッチを変更すると、速度の枠の情報も変更される。

    ノッチを増やした場合、増やした分はデフォルトで0になる。

3. 編成数を変更すると、右にある各車両の編成情報も変更される。

4. カラー数は、CS以後のファイルの場合、数のみ変更できる。

    LSはカラー数がないためサポート対象外、BSはCSVのみで改造できる。

5. 「この編成を修正する」ボタンで、右にある各車両の編成情報を修正できる。

6. 「保存する」ボタンで、右にある各車両の編成情報を保存できる

7. 「モデル情報の修正」ボタンで、設定されているモデル情報を変更できる

    この機能は、CSとRSのみできる。

8. 他にelse情報なども修正できる。

## モデル情報変更方法

![modelEdit](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/modelEdit.png)

※上記の機能は、Climax Stage、Rising Stageのみできる。

1. 車両の枠にある「モデル情報を修正」をクリックするとできる。

2. リストボックスをクリックして、修正、挿入、削除ができる。

    ただし、設定されているモデル、パンタ、COLは削除できない。

3. OKをクリックすると、各車両に設定したモデル情報が更新される。

## レンズフレア情報変更方法

![lens](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/lens.png)

1. レンズフレア情報と、テールランプの情報を修正できる


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
* Python 3.10.9 64bit
* pip 22.3.1 64bit
* PyInstaller 5.8.0 64bit
* 横1024×縦768ピクセル以上の画面解像度があるコンピュータ

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


* Q. 電車でDのゲームがあるが、指定したBINファイルがない。  
  
  * A. Lightning StageはDenD_Data102.Pack、

    Burning StageはPach006_ALL.Pack、

    Climax StageはPatch004.Pack、

    Rising StageはPatch_4th_4を

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

* Q. 編成数を伸ばしてみたら、エラーになる

  * A. ステージの初期配置位置から逆算して電車を構築するため、

    後ろに十分なレール領域がないと、エラーになる。

    また、Lightning Stage、Burning Stageは、理論上、無限に伸ばせるが

    Climax Stageは、1Pの場合、最大8両まで、

    Rising Stageは、1Pの場合、最大10両まで伸ばすことができる。

    2Pは（CPUのみ）、理論上、無限に伸ばせる。

### Windows 版実行バイナリ（ .exeファイル ）の作成方法

pyinstaller か Nuitka ライブラリをインストールする。 pip でも  easy_install  でも構わない。

下は、 pyinstaller を使用して、Windows 版実行バイナリ（ .exeファイル ）を作る例である。

````
> pyinstaller editor.py --onefile --noconsole --add-data "./dendData/*;./"
````

dist フォルダーが作られて、editor.exe が出力される。

### Virustotal

![virustotal](https://github.com/khttemp/dend-lbcr-editor/blob/main/image/virustotal.png)


以上。