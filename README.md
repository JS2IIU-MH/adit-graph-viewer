# ADIF Graph Viewer

ADIFファイルをアップロードして月次アクティビティグラフを表示するStreamlitアプリケーションです。


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://adif-graph-viewer.streamlit.app/)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 機能

- ADIFファイル（.adif, .adi）のアップロード（最大1GB）
- 月次QSO数のグラフ表示
- 生成されたグラフのPNGファイルとしてのダウンロード

どのようなものか試したい方はStreamlit Community Cloudにデプロイしたものがあります。以下のリンクからどうぞ。

[ADIF Graph Viewer · Streamlit](https://adif-graph-viewer.streamlit.app/)


## 必要条件

- Python 3.11以上
- pip（Pythonパッケージマネージャー）

## インストール方法

**注）不注意でリポジトリ名がadifにすべきところがaditになってしまいました。**

1. リポジトリをクローンまたはダウンロードします：
```bash
git clone https://github.com/JS2IIU-MH/adit-graph-viewer.git
cd adit-graph-viewer
```

2. 仮想環境を作成して有効化します：
```bash
python -m venv venv
source venv/bin/activate  # macOSの場合
# Windowsの場合: venv\Scripts\activate
```

3. 必要なパッケージをインストールします：
```bash
pip install -r requirements.txt
```

## 使用方法

1. アプリケーションを起動します：
```bash
streamlit run src/app.py
```

2. ブラウザが自動的に開き、アプリケーションが表示されます。

3. 「Choose an ADIF file」ボタンをクリックして、ADIFファイルをアップロードします。

4. ファイルが処理され、月次アクティビティグラフが表示されます。

5. グラフの下にある「Download image」リンクをクリックして、グラフをPNGファイルとしてダウンロードできます。

## 注意事項

- アップロード可能なファイルサイズは最大1GBです
- サポートされているファイル形式は .adif と .adi です
- グラフの生成には、ファイルサイズによって数秒から数分かかる場合があります

## 技術スタック

- [Streamlit](https://streamlit.io/) - Webアプリケーションフレームワーク
- [adiftools](https://github.com/JS2IIU-MH/adiftools-dev) - ADIFファイル処理ライブラリ
- [Matplotlib](https://matplotlib.org/) - グラフ描画ライブラリ

## ライセンス

MITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 作者

JS2IIU-MH

## 謝辞

- [adiftools](https://github.com/JS2IIU-MH/adiftools-dev) の開発者の関係者に感謝します
- [Streamlit](https://streamlit.io/) チームに感謝します 