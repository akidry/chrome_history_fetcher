# Chrome History Fetcher

Chrome閲覧履歴を取得・分析するためのツールです。

## 機能

- Chromeの閲覧履歴データベースからデータを抽出
- 訪問したWebサイトの統計情報を生成
- 閲覧パターンの視覚化

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
# 通常の使用方法
python chrome_history_fetcher.py

# Poetryを使用する場合
poetry run python chrome_history_fetcher.py

# カスタムオプション
python chrome_history_fetcher.py -n 200 -o history_data.csv
```

### データの可視化

```bash
# 通常の使用方法
python visualize_history.py history_data.csv

# Poetryを使用する場合
poetry run python visualize_history.py history_data.csv

# カスタムオプション
python visualize_history.py history_data.csv -o ./graphs -n 15 -d 60
```

## 必要条件

- Python 3.8+
- 依存パッケージ (pyproject.tomlまたはrequirements.txtを参照)

## ライセンス

MIT
