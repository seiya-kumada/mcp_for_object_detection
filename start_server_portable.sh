#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# プロジェクトディレクトリに移動
cd "$SCRIPT_DIR"

# uvがインストールされているかチェック
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 依存関係をインストール（初回のみ）
if [ ! -d ".venv" ]; then
    echo "Installing dependencies..."
    uv sync
fi

# MCPサーバーを起動
uv run python -m src
