#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome History Fetcher Constants
================================
Chrome履歴取得に関連する定数定義
"""

# Windows Epoch (1601-01-01) から Unix Epoch (1970-01-01) までの秒数
WINDOWS_UNIX_EPOCH_DIFFERENCE = 11644473600

# Chrome履歴データベースの時間スケールをミリ秒から秒に変換する係数
MILLISECONDS_TO_SECONDS = 1000000

# デフォルト設定値
DEFAULT_TOP_SITES = 10
DEFAULT_DAYS_HISTORY = 30
