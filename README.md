# **Fusion360_CreatePlanePlus**
Autodesk社 ソフト <b>"Fusion360" </b> のアドインです。

## 特徴:
標準機能として提供されていない、アバウトな平面作成コマンドを提供します。


## 設置:
こちらの手順に従い、アドインとして「CreatePlanePlus」フォルダを追加してください。

[Fusion 360にアドインまたはスクリプトをインストールする方法](
https://knowledge.autodesk.com/ja/support/fusion-360/troubleshooting/caas/sfdcarticles/sfdcarticles/JPN/How-to-install-an-ADD-IN-and-Script-in-Fusion-360.html)

## 使用:
アドイン実行すると、「基本フューチャー ソリッド」「基本フューチャー サーフェス」
「シートメタル」タブ時の「構築」パネルの一番下にコマンドが追加され、通常のコマンド同様に使用頂けます。

![追加コマンド](./images/menu.png)

履歴の使用（パラメトリック・ダイレクト）の有無に関わらず、御使用いただけます。


### [画面向きの平面] コマンド
クリックした部分を中心とし、画面の向き方向のコンストラクション平面を作成します。

### [法線方向の平面] コマンド
クリックした部分の面の法線方向に、コンストラクション平面を作成します。
「点で面に接する平面」コマンドに近いですが、事前に点を用意する必要はありません。


## 動作:
以下の環境にて確認。
+ Fusion360 Ver2.0.7830
+ Windows10 64bit Pro,Home

## 残された問題:
ルートコンポーネントと異なる原点を持つコンポーネントの要素を指定した場合、正しい位置に平面が作成されません。

## ライセンス:
MIT

## 謝辞:
+ こちらの便利な[フレームワーク](https://github.com/tapnair/Fusion360AddinSkeleton)を試用しました。
 Patrick Rainsberryさん、ありがとう。
+ [日本語フォーラム](https://forums.autodesk.com/t5/fusion-360-ri-ben-yu/bd-p/707)の皆さん、ありがとう。
+ アイコンが貧弱なので、センスの良い方提供して頂けると助かります・・・。