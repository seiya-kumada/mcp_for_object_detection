# MCP物体検出サーバー仕様書
Claude Codeに最初に作らせた仕様書です。

## 概要
MCP (Model Context Protocol) Python SDKを使用して、画像内の物体を検出するシンプルなMCPサーバーを構築します。このサーバーは、Claude Desktopアプリケーションと連携し、画像から物体を検出して、その矩形座標とラベルをJSON形式で返します。

## 機能要件（MVP版）

### 基本機能
- 画像ファイルのパスを受け取る
- YOLOv8を使用して物体検出を実行
- 検出された物体の矩形座標とラベルをJSON形式で返す

### MCPツール
- `detect_objects`: 画像から物体を検出する単一のツール

## 技術スタック

### コア技術
- **MCP Python SDK**: MCPサーバーの実装
- **Python 3.10+**: 開発言語
- **YOLOv8**: 物体検出モデル（Ultralyticsライブラリ使用）

### 依存ライブラリ
- `mcp`: MCPサーバー実装用
- `ultralytics`: YOLOv8モデル用
- `opencv-python`: 画像処理用
- `numpy`: 数値計算用

## プロジェクト構造
```
mcp_for_object_detection/
├── src/
│   ├── __init__.py       # パッケージ初期化
│   ├── __main__.py       # MCPサーバーのエントリーポイント
│   ├── server.py         # MCPサーバー実装
│   └── detector.py       # 物体検出ロジック
├── requirements.txt      # 依存関係
├── README.md            # プロジェクトドキュメント
└── specification.md     # この仕様書
```

## API仕様

### detect_objects
画像から物体を検出し、矩形座標とラベルを返します。

**入力パラメータ：**
- `image_path` (string, required): 画像ファイルのパス

**出力：**
```json
{
  "detections": [
    {
      "label": "person",
      "bbox": {
        "x": 100,
        "y": 150,
        "width": 200,
        "height": 300
      }
    },
    {
      "label": "car",
      "bbox": {
        "x": 400,
        "y": 200,
        "width": 150,
        "height": 100
      }
    }
  ]
}
```

## Claude Desktop統合

### 設定ファイル
Claude Desktopの設定ファイル（`claude_desktop_config.json`）に以下を追加：

```json
{
  "mcpServers": {
    "object-detection": {
      "command": "python",
      "args": ["-m", "mcp_for_object_detection"],
      "cwd": "/path/to/mcp_for_object_detection"
    }
  }
}
```

### 使用例
Claude Desktop内での使用例：
- 「/path/to/image.jpg の画像から物体を検出してください」
- 「この画像に何が写っているか検出してください: /Users/xxx/photo.png」

## エラーハンドリング
- 画像ファイルが見つからない場合のエラーメッセージ
- 無効な画像フォーマットの場合のエラーメッセージ

## 制約事項
- 画像ファイルはローカルファイルシステム上に存在する必要がある
- サポートする画像形式: JPEG, PNG
- YOLOv8がサポートする80クラスの物体のみ検出可能
