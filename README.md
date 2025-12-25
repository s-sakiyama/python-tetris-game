# Python Tetris Game

Python で開発された、Docker コンテナ化された Tetris ゲームです。Flask バックエンド、JavaScript フロントエンドで構築されています。

## 機能

- ✅ 7 種類のテトロミノ（I, O, T, S, Z, J, L）
- ✅ 回転、移動、硬落下（ハードドロップ）
- ✅ ラインクリア機能
- ✅ スコア計算（レベルボーナス付き）
- ✅ レベル進行システム
- ✅ 次のピース表示
- ✅ ゲームオーバー検出

## システム要件

- Docker
- Docker Compose
- または Python 3.11 以上

## インストール方法

### Docker で実行（推奨）

```bash
docker-compose up --build
```

ブラウザで http://localhost:5000 にアクセス

### ローカルで実行

```bash
# 依存関係をインストール
pip install -r requirements.txt

# Flask サーバーを起動
python app.py
```

ブラウザで http://localhost:5000 にアクセス

## ゲーム操作

| キー | 操作 |
|------|------|
| ← / → | ピースを左右に移動 |
| ↓ | ピースを下に移動 |
| Space | ピースを回転 |
| Up | ピースを硬落下（即座に配置） |
| P | ゲームを一時停止/再開 |

## プロジェクト構成

```
.
├── app.py                 # Flask サーバー（RESTful API）
├── game_logic.py          # ゲームロジック（Tetris コア）
├── renderer.py            # Pygame レンダラー（未使用）
├── main.py               # Pygame エントリーポイント（未使用）
├── requirements.txt       # Python 依存関係
├── Dockerfile            # Docker イメージ定義
├── docker-compose.yml    # Docker Compose 設定
├── templates/
│   └── index.html        # ゲーム UI テンプレート
├── static/
│   ├── game.js           # クライアント側ゲームコントローラー
│   └── style.css         # スタイルシート
└── tests/
    ├── test_game_logic.py # ユニットテスト（18 テスト）
    └── conftest.py       # pytest 設定
```

## API エンドポイント

### GET /
メインゲームページを返す

### GET /api/game/new
新しいゲームを初期化

**レスポンス:**
```json
{
  "board": [[0, 0, ...], ...],
  "current_piece": {...},
  "next_piece": {...},
  "score": 0,
  "level": 1,
  "lines": 0
}
```

### GET /api/game/state
現在のゲーム状態を取得

### POST /api/game/move/<direction>
ピースを移動

**パラメータ:** `direction` - `left`, `right`, `down`, `rotate`, `drop`

### POST /api/game/tick
ゲームを 1 ティック進める

## テスト実行

```bash
# すべてのテストを実行
pytest tests/

# テスト結果を詳細表示
pytest tests/ -v

# カバレッジを確認
pytest tests/ --cov=. --cov-report=html
```

## テスト内容

- ゲーム初期化（9 テスト）
- ピース移動（8 テスト）
- ピース回転（3 テスト）
- ラインクリア（5 テスト）
- ゲームオーバー（2 テスト）
- スコア計算（3 テスト）
- ピースデータ（1 テスト）

**全 18 テスト - すべてパス ✅**

## ゲーム仕様

| 項目 | 値 |
|------|-----|
| ボード幅 | 10 ブロック |
| ボード高さ | 20 ブロック |
| ゲームティック間隔 | 500 ms |
| テトロミノ数 | 7 種類 |

### スコア計算ルール

- 1 行クリア: `40 × (レベル + 1)`
- 2 行クリア: `100 × (レベル + 1)`
- 3 行クリア: `300 × (レベル + 1)`
- 4 行クリア（テトリス）: `1200 × (レベル + 1)`
- ハードドロップボーナス: `2 × ドロップ距離`

### レベル進行

```
レベル = 1 + (クリア行数 // 10)
```

## 技術スタック

- **バックエンド:** Python 3.11, Flask 3.0.0
- **フロントエンド:** HTML5, CSS3, JavaScript (Vanilla)
- **テスト:** pytest 7.4.3
- **コンテナ:** Docker, Docker Compose
- **ゲームエンジン:** 独自実装

## 開発者向け情報

### ゲームロジック（game_logic.py）

`TetrisGame` クラスが主要なゲーム機能を提供：

```python
game = TetrisGame()
game.move('left')          # ピースを左移動
game.move('rotate')        # ピースを回転
game.move('drop')          # ピースをハードドロップ
game.tick()                # ゲームを 1 ティック進める
state = game.get_state()   # ゲーム状態を取得
```

### API サーバー（app.py）

Flask で実装された RESTful API サーバー：

```python
from app import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## ライセンス

MIT License

## 作成者

s-sakiyama

## 更新履歴

- 2025-12-25: 初版リリース
  - Python ゲームロジック実装
  - Flask Web サーバー実装
  - Docker コンテナ化
  - 包括的なテストスイート追加
  - 日本語 UI 対応
