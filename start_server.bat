@echo off
setlocal

REM スクリプトのディレクトリを取得
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM uvがインストールされているかチェック
uv --version >nul 2>&1
if errorlevel 1 (
    echo Error: uv is not installed. Please install uv first:
    echo curl -LsSf https://astral.sh/uv/install.sh ^| sh
    pause
    exit /b 1
)

REM 依存関係をインストール（初回のみ）
if not exist ".venv" (
    echo Installing dependencies...
    uv sync
)

REM MCPサーバーを起動
uv run python -m src
