# AES-256 ファイル暗号化・復号ツール

## 概要

このツールは、AES-256（CFBモード）によるファイルの暗号化・復号を行うPython製のGUIアプリケーションです。

---

## 必要環境

- Python 3.7 以上

---
~~## Zipファイルで仮想環境ごとダウンロードする場合~~

~~仮想環境の構築をせずにZipファイルで簡単にセットアップする場合は[使い方.mdを参照](./使い方.md)~~　←PCの環境によってブレが発生するため、使用できないようにしました。
## インストール・実行方法

### 1. 仮想環境の作成・有効化

実行前に、**仮想環境を作成してアクティベート**してください。  

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python -m venv venv
source venv/bin/activate
```

### 2. 依存ライブラリのインストール

```bash
pip install pycryptodome
```

### 3. 実行

```bash
python main.py
```
