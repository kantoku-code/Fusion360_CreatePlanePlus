# **Fusion360_CreatePlanePlus**
Autodesk社 ソフト <b>"Fusion360" </b> のアドインです。

## 特徴:
標準機能として提供されていない、アバウトな平面作成コマンドを提供します。


## **インストール**:
インストールする際は、zip ファイルをダウンロード/展開後 "CreatePlanePlus" フォルダをアドインとして登録してください。

アドインの登録は、[こちら](https://kantoku.hatenablog.com/entry/2021/02/15/161734)の手順に従ってください。


## 使用:
アドイン実行すると、「ソリッド」「サーフェス」「メッシュ」「シートメタル」「プラスチック」タブ時の「構築」パネルの平面の中にコマンドが追加され、通常のコマンド同様に使用頂けます。


## **リスト**:
コマンドについては、各コマンド毎の説明をご覧ください。

+ [法線方向の平面](./CreatePlanePlus/commands/NormalPlane/) : クリックした部分の面の法線方向に平面を作成します。「点で面に接する平面」コマンドに近いですが、事前に点を用意する必要はありません。
+ [画面向きの平面](./CreatePlanePlus/commands/ViewPlane/) : クリックした部分を中心とし、画面の向き方向のコンストラクション平面を作成します。
+ [パス上の点平面](./CreatePlanePlus/commands/PointOnPathPlane/) : "パスに沿った平面" に近い操作ですが、パス上の点の位置で平面を作成します。
+ [極平面](./CreatePlanePlus/commands/PolarPlane/) : ボディと方向を指定し、極平面を作成します。



## 動作:
以下の環境にて確認。
+ Fusion360 Ver2.0.13866
+ Windows10 64bit Pro,Home

## ライセンス:
MIT

## 謝辞:
+ [日本語フォーラム](https://forums.autodesk.com/t5/fusion-360-ri-ben-yu/bd-p/707)の皆さん、ありがとう。
+ アイコンが貧弱なので、センスの良い方提供して頂けると助かります・・・。