# これはなに？

このプロジェクトは日本郵便が公開している**郵便番号**の表データの最新を取得してJSONデータに落とし込むスクレイピングツールのプロジェクトです。

データはこちらから取得できます。  
https://www.post.japanpost.jp/zipcode/dl/utf-zip.html

# JSONデータ

生成済みのデータを利用する場合はdistフォルダを参照してください。

生成済ファイル一覧

| ファイル名                     | 説明                        |
|---------------------------|---------------------------|
| postal_codes.json         | CSVをそのままJSON形式にしたデータ      |
| postal_code_map.json      | CSVを郵便番号でマップ形式にしたJSONデータ |

# 変換ルール
1. oazaはoaza_originalに全て移動
2. 「以下に掲載がない場合」、「（次のビルを除く）」は削除
3. oazaの()内は全て大字から分離してoaza_annotationに移動
4. oazaの「」内は全て削除
5. oazaの()内のA丁目〜Z丁目はリストに展開
6. oazaの番地は展開しない
   1-1000と、範囲が多すぎるのと、実在しない番地がありそう。1000〜と閉じられていないケースもあったため
7. oazaの地割は展開するのとしないものがある
   地割は地名A地割や地名(第A地割〜第Z地割)、○○台A地割などイレギュラーが多いため

test/test_extract.py に変換のテストコードがあります。

※当方、住所の有識者ではないため、変換ルールにご意見ある場合はお気軽にご連絡ください。

# 開発者向け

## 依存モジュール

Pythonの下記モジュールを利用しています。

* Scrapy
* Pandas
* tomli

## JSON生成方法

Dockerを使います。Pythonを直接使う場合は後述の実行方法を参照してください。

1. ダウンロードしたプロジェクトフォルダに移動します。

```shell
$ cd ダウンロードしたpostal_code_jsonのフォルダ
```

2. Dockerイメージをビルドします。

```shell
$ docker build -t postal_code_json:latest .
```

3. Dockerイメージを実行します。

```shell
$ `docker run --rm --mount type=bind,source=./dist,target=/postal_code_json/dist -t postal_code_json:latest`
```

4. distフォルダにjsonファイルが生成していたら成功です。

```shell
$ ls ./dist
```

## 実行方法

Scrapyを使って実行します。

1. poetryをインストールします。

```shell
$ pythom -m pip install poetry
```

2. poetryで依存モジュールをインストールします。

```shell
$ poetry install
```

3. scrapyのプロジェクトフォルダに移動します。

```shell
$ cd scrape
```

4. poetryの実行環境を使ってscrapyを実行します。

```shell
$ poetry run scrapy crawl postal_code_spider
```

# LICENSE

本プロジェクトはApache License, Version2.0ライセンスで公開しています。  
postal_code_json by Newmarket Inc. is licensed under the Apache License, Version2.0
