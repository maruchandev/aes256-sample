@echo off
REM 仮想環境が存在しない場合は作成
if not exist venv (
    echo === 仮想環境を作成します ===
    python -m venv venv
)

REM 仮想環境をアクティベート
call venv\Scripts\activate

REM 依存ライブラリをインストール
echo === 必要なライブラリをインストールします ===
pip install --upgrade pip
pip install pycryptodome

REM プログラムを実行
echo === プログラムを起動します ===
python main.py

pause
