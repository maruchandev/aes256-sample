@echo off
setlocal

REM ===== 設定 =====
set REPO_URL=https://github.com/maruchandev/aes256-sample/archive/refs/heads/main.zip
set ZIP_FILE=aes256-sample.zip
set PROJECT_DIR=aes256-sample-main

REM ===== GitHub からソース取得 =====
echo === GitHub からソースを取得します ===
curl -L %REPO_URL% -o %ZIP_FILE%
if %ERRORLEVEL% neq 0 (
    echo [ERROR] curl に失敗しました。
    pause
    exit /b 1
)

REM ===== ZIP を展開 =====
echo === ZIP を展開します ===
powershell -Command "Expand-Archive -Force '%ZIP_FILE%'"
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ZIP 展開に失敗しました。
    pause
    exit /b 1
)

REM ===== プロジェクトディレクトリに移動 =====
cd %PROJECT_DIR%
if ERRORLEVEL 1 (
    echo [ERROR] プロジェクトフォルダ %PROJECT_DIR% が見つかりません。
    pause
    exit /b 1
)

REM ===== 仮想環境の作成 =====
if not exist venv (
    echo === 仮想環境を作成します ===
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

REM ===== 仮想環境の有効化 =====
echo === 仮想環境を有効化します ===
call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 仮想環境の有効化に失敗しました。
    pause
    exit /b 1
)

REM ===== 依存ライブラリのインストール =====
echo === 依存ライブラリをインストールします ===
pip install --upgrade pip
pip install pycryptodome
if %ERRORLEVEL% neq 0 (
    echo [ERROR] ライブラリのインストールに失敗しました。
    pause
    exit /b 1
)

REM ===== プログラムを実行 =====
echo === プログラムを実行します ===
python main.py
if %ERRORLEVEL% neq 0 (
    echo [ERROR] プログラムの実行に失敗しました。
    pause
    exit /b 1
)

pause
