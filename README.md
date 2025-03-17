# Chrome History Fetcher

Chrome閲覧履歴を取得・分析するためのツールです。

## 機能

- Chromeの閲覧履歴データベースからデータを抽出
- 訪問したWebサイトの統計情報を生成
- 閲覧パターンの視覚化
- 履歴データを日付付きファイル名で専用フォルダに保存

## インストール方法

### 通常のインストール方法

```bash
git clone https://github.com/akidry/chrome_history_fetcher.git
cd chrome_history_fetcher
pip install -r requirements.txt
```

### Poetry を使ったインストール方法

```bash
git clone https://github.com/akidry/chrome_history_fetcher.git
cd chrome_history_fetcher

# Poetryがインストールされていない場合はインストール
# curl -sSL https://install.python-poetry.org | python3 -

# Poetry環境をセットアップ
poetry install

# Poetry環境内でコマンドを実行
poetry run python chrome_history_fetcher.py
```

## 使い方

### 履歴データの取得

```bash
# 通常の使用方法（すべての履歴を取得、history_dataフォルダに日付付きファイル名で保存）
python chrome_history_fetcher.py

# Poetryを使用する場合
poetry run python chrome_history_fetcher.py

# 特定の数のエントリのみ取得する場合
python chrome_history_fetcher.py -n 500

# カスタム出力先を指定
python chrome_history_fetcher.py -o ./my_folder/history_data.csv

# 出力を保存しない場合
python chrome_history_fetcher.py --no-save
```

### データの可視化

```bash
# 通常の使用方法
python visualize_history.py history_data/chrome_history_20250317_123456.csv

# Poetryを使用する場合
poetry run python visualize_history.py history_data/chrome_history_20250317_123456.csv

# カスタムオプション
python visualize_history.py history_data.csv -o ./graphs -n 15 -d 60
```

## オプション

### chrome_history_fetcher.py

- `-n, --entries` : 取得するエントリー数（デフォルト: すべて取得）
- `-p, --path` : 履歴データベースへのカスタムパス
- `-o, --output` : 出力先CSVファイル名（指定しない場合はhistory_dataフォルダに日付付きで保存）
- `--no-save` : CSVファイルに保存しない

### visualize_history.py

- `-o, --output_dir` : 出力グラフの保存先ディレクトリ
- `-n, --top_n` : 表示するトップドメインの数
- `-d, --days` : 日別アクティビティを表示する日数

## 必要条件

- Python 3.8.1+
- 依存パッケージ (pyproject.tomlまたはrequirements.txtを参照)

## ライセンス

MIT
