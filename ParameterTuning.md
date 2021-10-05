# Parameter tuning

## コンテンツ

1. GCSにデータ、プログラムをアップロードする
2. クラスタを生成する
3. アップロードしたデータを入れたPersistent volumeを準備する
4. スクリプト実行用のPodを生成、スクリプトをダウンロードする
5. SQLを実行するPodを生成する
6. スクリプトを実行
7. 完了要件に達したら、SQLからデータを抽出、GCSにアップロードする
8. クリーンアップでGCS以外の全てのデータを削除する

## 事前準備
Localでgcloudを使えるように事前設定する。kubectlコマンドも利用できるように設定する。
``` bash
# setting gcloud
gcloud init

# Update components
gcloud components update
gcloud components update kubectl
```

## GCSにデータ、プログラムをアップロードする




## クラスタを生成する

