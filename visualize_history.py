#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome History Visualizer
========================
Chromeブラウザの閲覧履歴を可視化するためのスクリプト
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
from utils.constants import DEFAULT_TOP_SITES, DEFAULT_DAYS_HISTORY

# スタイル設定
sns.set(style="darkgrid")


def load_history_data(file_path):
    """CSVまたはExcelから履歴データを読み込む"""
    file_path = Path(file_path)
    
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("サポートされていないファイル形式です。CSVまたはExcelファイルを使用してください。")
    
    # 日時列を適切に処理
    if 'visit_time' in df.columns:
        df['visit_time'] = pd.to_datetime(df['visit_time'])
        
    return df


def plot_time_distribution(df, output_path=None):
    """時間帯別の閲覧回数を可視化"""
    if 'visit_time' not in df.columns:
        print("警告: 'visit_time'カラムがデータに存在しません")
        return
    
    # 時間帯ごとの集計
    df['hour'] = df['visit_time'].dt.hour
    hourly_counts = df['hour'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=hourly_counts.index, y=hourly_counts.values)
    plt.title("時間帯別のWebサイト訪問回数")
    plt.xlabel("時間帯")
    plt.ylabel("訪問回数")
    plt.xticks(range(24))
    
    if output_path:
        plt.savefig(output_path)
    plt.show()


def plot_domain_breakdown(df, top_n=DEFAULT_TOP_SITES, output_path=None):
    """トップドメインのパイチャート"""
    if 'domain' not in df.columns and 'url' in df.columns:
        # ドメイン列がない場合は作成
        df['domain'] = df['url'].str.extract(r'https?://(?:www\.)?([^/]+)')
    
    domain_counts = df['domain'].value_counts().head(top_n)
    others_count = df['domain'].value_counts().iloc[top_n:].sum()
    
    # 「その他」カテゴリを追加
    if others_count > 0:
        domain_counts['その他'] = others_count
    
    plt.figure(figsize=(10, 8))
    plt.pie(domain_counts.values, labels=domain_counts.index, autopct='%1.1f%%', 
            shadow=True, startangle=90)
    plt.axis('equal')
    plt.title(f"訪問したドメインの内訳 (Top {top_n})")
    
    if output_path:
        plt.savefig(output_path)
    plt.show()


def plot_daily_activity(df, days=DEFAULT_DAYS_HISTORY, output_path=None):
    """日別の閲覧活動を可視化"""
    if 'visit_time' not in df.columns:
        print("警告: 'visit_time'カラムがデータに存在しません")
        return
    
    # 過去X日間のデータに絞る
    today = pd.Timestamp.now().normalize()
    start_date = today - pd.Timedelta(days=days)
    
    mask = df['visit_time'] >= start_date
    recent_df = df[mask].copy()
    
    if len(recent_df) == 0:
        print(f"警告: 過去{days}日間のデータがありません")
        return
    
    # 日付ごとの集計
    recent_df['date'] = recent_df['visit_time'].dt.date
    daily_counts = recent_df.groupby('date').size()
    
    # 連続した日付のインデックスを作成
    date_range = pd.date_range(start=start_date, end=today)
    daily_counts = daily_counts.reindex(date_range, fill_value=0)
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(x=daily_counts.index, y=daily_counts.values, marker='o')
    plt.title(f"過去{days}日間の日別アクティビティ")
    plt.xlabel("日付")
    plt.ylabel("訪問回数")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    plt.show()


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Chrome閲覧履歴の可視化ツール')
    parser.add_argument('file', type=str, help='閲覧履歴データファイル（CSVまたはExcel）')
    parser.add_argument('-o', '--output_dir', type=str, default='.',
                        help='出力グラフの保存先ディレクトリ（デフォルト: カレントディレクトリ）')
    parser.add_argument('-n', '--top_n', type=int, default=DEFAULT_TOP_SITES,
                        help=f'表示するトップドメインの数（デフォルト: {DEFAULT_TOP_SITES}）')
    parser.add_argument('-d', '--days', type=int, default=DEFAULT_DAYS_HISTORY,
                        help=f'日別アクティビティを表示する日数（デフォルト: {DEFAULT_DAYS_HISTORY}）')
    
    args = parser.parse_args()
    
    try:
        # データ読み込み
        df = load_history_data(args.file)
        print(f"データを読み込みました: {len(df)}件のレコード")
        
        # 出力ディレクトリを作成
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # 時間帯別分布
        time_output = output_dir / 'time_distribution.png'
        plot_time_distribution(df, time_output)
        print(f"時間帯別分布グラフを保存しました: {time_output}")
        
        # ドメイン内訳
        domain_output = output_dir / 'domain_breakdown.png'
        plot_domain_breakdown(df, args.top_n, domain_output)
        print(f"ドメイン内訳グラフを保存しました: {domain_output}")
        
        # 日別アクティビティ
        daily_output = output_dir / 'daily_activity.png'
        plot_daily_activity(df, args.days, daily_output)
        print(f"日別アクティビティグラフを保存しました: {daily_output}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
