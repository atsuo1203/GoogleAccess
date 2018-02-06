# GoogleAccess

## 環境

* python 3.6.3

## インストール

```
$ pip install -r requirements.txt
```

## googleAPI準備

* [Google API Console](https://console.developers.google.com/)にアクセスして、Service Account Keyを発行。

* [参考サイト](http://scuel-developer.hatenablog.jp/entry/2016/06/10/gspread%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6python%E3%81%8B%E3%82%89Google_Spreadsheets%E3%82%92%E7%B7%A8%E9%9B%86%E3%81%99%E3%82%8B)

## ファイル準備

```
$ touch projectName.json config.yaml
```

* 上のコマンド実行後に、下記のようにファイルを修正。

* `projectName.json`の中身はService Account Key作成時にダウンロード出来るので、それをコピペ。

`projectName.json`

``` projectName.json
{
  "type": "service_account",
  "project_id": "*********",
  "private_key_id": "*****",
  "private_key": "-----BEGIN PRIVATE KEY-----\n**************\n-----END PRIVATE KEY-----\n",
  "client_email": "********@*******.iam.gserviceaccount.com",
  "client_id": "**************",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/*******************.iam.gserviceaccount.com"
}
```

` confing.yaml`
``` confing.yaml
# spreadsheet
sheet1:
  sheet_id: ***************************************
  description: spreadsheet1


# user
user1:
  id: *******************
  email: example@gmail.com
  description: user1
```

## 起動
```
$ python manage.py
```
