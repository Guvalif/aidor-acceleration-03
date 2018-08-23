AIDOR ACCELERATION 基礎知識講座 第3回 | サンプルプログラム
===============================================================================

What's This?
-------------------------------------------------------------------------------

IoT・ロボットビジネス創出プログラム「[AIDOR ACCELERATION](https://www.imedio.or.jp/acceleration)」における、
2018年度 基礎知識講座 第3回で使用したサンプルプログラムです。


Getting Started
-------------------------------------------------------------------------------

第2回の[セットアップ手順](https://github.com/Guvalif/imedio_0801/blob/master/README.md)もあわせて行ってください。

Raspberry Piにログインした後、下記画像 青線部内のアイコンをクリックし**ターミナル**を開きます。

![](.assets/desktop.png)

**ターミナル**上で、以下のコマンドを入力します：

```sh
sudo pip install paste boto3 AWSIoTPythonSDK
```

これにより、

- `paste`: 同時アクセス可能なHTTPサーバを作成するためのライブラリ
- `boto3`: AWSのサービスをPythonから制御するためのライブラリ
- `AWSIoTPythonSDK`: AWS IoT CoreをPythonから制御するためのライブラリ

以上3点がインストールされます。


How to Use
-------------------------------------------------------------------------------

[ダウンロードリンク](https://github.com/Guvalif/imedio_0822/archive/master.zip)をクリックすることで、
プログラムを一式ダウンロードできます。

**ターミナル**上で`sudo idle`と入力し、**Python 2 IDLE**を起動します。
その後、メニューから`File -> Open...`とたどることで、それぞれのプログラムを開くことができます。

プログラムを実行するには、メニューから`Run -> Run Module`とたどります。

なお、同梱されるプログラムは以下の通りです：

- `http_v2`
    - `example_http_v2.py`: センサ・アクチュエータのインターネットリソース化とコンテンツ配信を行うプログラム
    - `index_v1.html`: HTMLのみを記述したGUI
    - `index_v2.html`: HTML/CSSを記述したGUI
    - `index_v3.html`: HTML/CSS/JavaScriptを記述したGUI
- `aws`
    - `aws_credentials.py`: AWSの認証情報を記述するライブラリ
    - `example_s3.py`: S3にセンシングしたデータをアップロードするプログラム
    - `example_aws.py`: `example_s3.py` の挙動に加えて、AWS IoT Coreとのメッセージ送受信，およびサーボモータを動かすプログラム
    - `root-ca.crt`: AWS IoT Coreへアクセスするためのルート証明書
- `aws_gui`
    - `assets`: CSS/JavaScript/画像素材を配置したフォルダ
    - `404.html`: エラーページを記述したHTMLファイル
    - `index.html`: GUIを記述したHTMLファイル


Copyright (c) 2018,
-------------------------------------------------------------------------------

- [PLEN Project Company Inc.](https://plen.jp)
- [Kazuyuki TAKASE](https://github.com/Guvalif)

This software is released under [the MIT License](http://opensource.org/licenses/mit-license.php).