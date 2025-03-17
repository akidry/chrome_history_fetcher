#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome History Fetcher
=====================
Chromeブラウザの閲覧履歴を取得・分析するためのツール
"""

import os
import sqlite3
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime


def get_chrome_history_path():
    """Chromeの履歴データベースのパスを取得する"""
    home = Path.home()
    
    # オペレーティングシステムに応じたパスを返す
    if os.name == 'nt':  # Windows
        return home / 'AppData/Local/Google/Chrome/User Data/Default/History'
    elif os.name == 'posix':  # macOS / Linux
        if os.path.exists(home / 'Library/Application Support/Google/Chrome'):  # macOS
            return home / 'Library/Application Support/Google/Chrome/Default/History'
        else:  # Linux
            return home / '.config/google-chrome/Default/History'
    else:
        raise OSError("サポートされていないOSです")


def fetch_history(history_path=None, n_entries=None):
    """
    Chrome履歴データベースから閲覧履歴を取得する
    
    Parameters:
    -----------
    history_path : str or Path, optional
        履歴データベースへのパス。指定しない場合は自動検出する。
    n_entries : int, optional
        取得するエントリー数（指定しない場合はすべて取得）
        
    Returns:
    --------
    pandas.DataFrame
        取得した履歴データ
    """
    if history_path is None:
        history_path = get_chrome_history_path()
    
    # データベースファイルをコピーして使用（ロックを回避）
    history_path = Path(history_path)
    temp_path = Path('temp_history_db')
    
    # 元のファイルが存在するか確認
    if not history_path.exists():
        raise FileNotFoundError(f"履歴ファイルが見つかりません: {history_path}")
    
    # 一時ファイルにコピー
    import shutil
    shutil.copy2(history_path, temp_path)
    
    try:
        # SQLiteデータベースに接続
        conn = sqlite3.connect(temp_path)
        
        # 履歴データを取得
        limit_clause = f"LIMIT {n_entries}" if n_entries is not None else ""
        query = f"""
        SELECT
            urls.url,
            urls.title,
            datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time,
            visits.visit_duration
        FROM urls
        JOIN visits ON urls.id = visits.url
        ORDER BY visits.visit_time DESC
        {limit_clause}
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
        
    finally:
        # 一時ファイルを削除
        if temp_path.exists():
            os.remove(temp_path)


def analyze_history(df):
    """履歴データの簡単な分析を行う"""
    # 訪問回数の多いサイトを抽出
    top_sites = df['url'].value_counts().head(10)
    
    # ドメインごとの訪問回数
    df['domain'] = df['url'].str.extract(r'https?://(?:www\.)?([^/]+)')
    top_domains = df['domain'].value_counts().head(10)
    
    return {
        'top_sites': top_sites,
        'top_domains': top_domains
    }


def get_default_output_path():
    """日付を含むデフォルトの出力パスを返す"""
    # カレントディレクトリに 'history_data' フォルダを作成
    output_dir = Path('history_data')
    output_dir.mkdir(exist_ok=True)
    
    # 現在の日時を含むファイル名を生成
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"chrome_history_{timestamp}.csv"
    
    return output_dir / filename


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Chrome閲覧履歴を取得・分析するツール')
    parser.add_argument('-n', '--entries', type=int, default=None,
                        help='取得するエントリー数（デフォルト: すべて）')
    parser.add_argument('-p', '--path', type=str, default=None,
                        help='履歴データベースへのカスタムパス')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='出力先CSVファイル名（指定しない場合はhistory_dataフォルダに日付付きで保存）')
    parser.add_argument('--no-save', action='store_true',
                        help='CSVファイルに保存しない')
    
    args = parser.parse_args()
    
    try:
        # 履歴を取得
        df = fetch_history(args.path, args.entries)
        
        # 結果を表示
        print(f"取得した履歴エントリー数: {len(df)}")
        
        # 分析を実行
        analysis = analyze_history(df)
        
        print("\n訪問回数の多いサイト（Top 10）:")
        print(analysis['top_sites'])
        
        print("\nドメインごとの訪問回数（Top 10）:")
        print(analysis['top_domains'])
        
        # CSVに出力（--no-saveが指定されていない場合）
        if not args.no_save:
            # 出力先が指定されていない場合は日付付きのデフォルトパスを使用
            output_path = args.output if args.output else get_default_output_path()
            
            # 出力先ディレクトリが存在しない場合は作成
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"\n履歴データを {output_path} に保存しました")
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
