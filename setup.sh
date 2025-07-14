#!/bin/bash

set -e

echo "🚀 MCP Object Detection Server セットアップ開始"

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# uvのインストールチェック
if ! command -v uv &> /dev/null; then
    echo "📦 uvをインストール中..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uvのインストールが完了しました"
    echo "⚠️  新しいターミナルを開くか、以下のコマンドを実行してください："
    echo "source ~/.bashrc  # または source ~/.zshrc"
    exit 0
fi

echo "✅ uvは既にインストールされています"

# 依存関係のインストール
echo "📦 依存関係をインストール中..."
uv sync

# 実行権限を付与
echo "🔧 スクリプトに実行権限を付与中..."
chmod +x start_server.sh
chmod +x start_server_debug.sh
chmod +x start_server_portable.sh
chmod +x setup.sh

# テスト実行
echo "🧪 テストを実行中..."
uv run python test_detector.py

echo "✅ セットアップが完了しました！"
echo ""
echo "使用方法："
echo "1. スタンドアロンテスト: uv run python test_detector.py"
echo "2. MCPサーバー起動: ./start_server_portable.sh"
echo "3. Claude Desktop設定例:"
echo "   {"
echo '     "mcpServers": {'
echo '       "object-detection": {'
echo '         "command": "'$SCRIPT_DIR'/start_server_portable.sh"'
echo '       }'
echo '     }'
echo '   }'
