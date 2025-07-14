# MCP Object Detection Server

YOLOv8を使用した物体検出MCPサーバー。Claude Desktopから画像内の物体を検出できます。

## 機能

- YOLOv8による高速物体検出（80クラス対応）
- Claude DesktopとのMCPプロトコル統合
- JSON形式での検出結果出力
- 矩形座標と信頼度スコア付き

## インストール

### 必要条件

- Python 3.11以上
- uv (Pythonパッケージマネージャー)
- macOS (他のOSでも動作可能ですが、設定が異なる場合があります)

### セットアップ

#### 自動セットアップ（推奨）

```bash
git clone https://github.com/yourusername/mcp_for_object_detection.git
cd mcp_for_object_detection
chmod +x setup.sh
./setup.sh
```

#### 手動セットアップ

1. リポジトリのクローン：
```bash
git clone https://github.com/yourusername/mcp_for_object_detection.git
cd mcp_for_object_detection
```

2. uvのインストール（未インストールの場合）：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. 依存関係のインストール：
```bash
uv sync
```

## 使用方法

### スタンドアロンでのテスト

```bash
# 物体検出のテスト
uv run python test_detector.py

# MCPサーバーの起動（デバッグ用）
uv run python -m src
```

### Claude Desktopとの統合

1. Claude Desktopの設定ファイルを編集：
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 以下の設定を追加：
```json
{
    "mcpServers": {
        "object-detection": {
            "command": "/path/to/mcp_for_object_detection/start_server.sh"
        }
    }
}
```

3. Claude Desktopを再起動

4. Claude Desktop内で使用：
```
画像 /path/to/image.jpg から物体を検出してください
```

## スクリプトの説明

### start_server_portable.sh（推奨）

環境に依存しないポータブルな起動スクリプトです。

```bash
#!/bin/bash
# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# uvがインストールされているかチェック
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed"
    exit 1
fi

# 依存関係をインストール（初回のみ）
if [ ! -d ".venv" ]; then
    uv sync
fi

# MCPサーバーを起動
uv run python -m src
```

**機能：**
- 環境に依存しない（絶対パスを使用しない）
- uvの存在チェック
- 自動依存関係インストール
- Claude Desktopからの実行用に設計

### start_server.sh

MCPサーバーを起動するための基本的なシェルスクリプトです。

```bash
#!/bin/bash
cd /Users/kumada/Projects/mcp_for_object_detection
/Users/kumada/.local/bin/uv run python -m src
```

**機能：**
- プロジェクトディレクトリに移動
- uvを使用してPython仮想環境内でMCPサーバーを起動
- Claude Desktopからの実行用に設計

**使用理由：**
- Claude Desktopは直接uvコマンドを見つけられない場合がある
- フルパスを使用して確実に実行
- 作業ディレクトリを正しく設定

### start_server_debug.sh

デバッグ情報をログファイルに記録するバージョンです。

```bash
#!/bin/bash
echo "Starting MCP Object Detection Server..." >> /tmp/mcp_object_detection.log
echo "Date: $(date)" >> /tmp/mcp_object_detection.log
echo "PWD: $(pwd)" >> /tmp/mcp_object_detection.log
echo "PATH: $PATH" >> /tmp/mcp_object_detection.log

cd /Users/kumada/Projects/mcp_for_object_detection
/Users/kumada/.local/bin/uv run python -m src 2>> /tmp/mcp_object_detection.log
```

**機能：**
- サーバー起動時の環境情報をログに記録
- エラー出力を `/tmp/mcp_object_detection.log` にリダイレクト
- トラブルシューティング用

**ログの確認方法：**
```bash
tail -f /tmp/mcp_object_detection.log
```

### test_detector.py

物体検出機能を直接テストするためのスクリプトです。

**機能：**
- `images/test.png` を使用して検出テスト
- 検出結果を見やすい形式で表示
- JSON形式での出力も確認可能

## プロジェクト構造

```
mcp_for_object_detection/
├── src/
│   ├── __init__.py       # パッケージ初期化
│   ├── __main__.py       # MCPサーバーのエントリーポイント
│   ├── server.py         # MCPサーバー実装
│   └── detector.py       # YOLOv8物体検出ロジック
├── images/
│   └── test.png          # テスト用画像
├── start_server.sh       # 通常起動用スクリプト
├── start_server_debug.sh # デバッグ起動用スクリプト
├── start_server_portable.sh # ポータブル起動用スクリプト（推奨）
├── start_server.bat      # Windows用起動スクリプト
├── setup.sh              # 自動セットアップスクリプト
├── test_detector.py      # 検出機能テストスクリプト
├── pyproject.toml        # uvプロジェクト設定
├── requirements.txt      # Python依存関係（後方互換性）
├── README.md            # このファイル
└── specification.md     # 仕様書
```

## トラブルシューティング

### "command not found" エラー

- `start_server.sh` 内のuvパスが正しいか確認
- `which uv` でuvの場所を確認し、必要に応じてパスを更新

### Claude Desktopで認識されない

1. 設定ファイルのJSON構文を確認
2. `start_server.sh` に実行権限があるか確認：
   ```bash
   chmod +x start_server.sh
   ```
3. デバッグ版を使用してログを確認：
   ```bash
   # claude_desktop_config.jsonで start_server_debug.sh を指定
   tail -f /tmp/mcp_object_detection.log
   ```

### YOLOモデルのダウンロード

初回実行時、YOLOv8nモデル（約6.5MB）が自動的にダウンロードされます。

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを作成して変更内容を説明してください。
