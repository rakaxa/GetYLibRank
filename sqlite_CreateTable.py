# -*- coding: utf-8 -*-
import sys
import sqlite3

# 
# テーブル作成 
# 

if __name__ == '__main__':
  # 
  # 第1引数 : データベースへのパス
  # 
  if len(sys.argv) != 2:
    sys.exit("usage : > python sqlite_CreateTable.py [DatabaseName]")
  db_path = sys.argv[1]

  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  query = '''create table YokohamaLibraryTop50 (date text, rank integer, title text, author text, reserve integer, primary key(date, rank, title))'''
  c.execute(query) 
