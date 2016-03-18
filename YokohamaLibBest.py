#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib.request
import datetime
import re
import sqlite3

########################################
# URLからページを取得する関数
# url : URL
# RET : オープンしたURLのハンドラ
########################################
def GetPage(url):
  return urllib.request.urlopen(url)

########################################
# 対象行の情報が有用かどうかを判定
# line : 対象行
# RET  : 有用のとき、対象文字列
#        不要のとき、False
########################################
def CheckLine(line):
  s = re.match('^\<td\>(.*?)\<\/td\>$', line.decode('Shift_JIS'))
  if s:
    return s.group(1)
  else:
    return False

########################################
# "／"以降を削除する
# str : 対象文字列
# RET : "／"以降を削除した文字列
########################################
def DeleteAfterSlash(str):
  ss = re.match('(.*?)\\uFF0F.*', str)
  if ss:
    str = ss.group(1)
  return str

########################################
# ランキング情報を取得
# str : 対象文字列
# RET : ランキング値
########################################
def GetRank(str):
  return int(str)

########################################
# タイトルを取得
# str : 対象文字列
# RET : タイトル
########################################
def GetTitle(str):
  title = re.sub('\<.*?\>', '', str) # HTMLタグを削除
  return DeleteAfterSlash(title)

########################################
# 作者を取得
# str : 対象文字列
# RET : 作者
########################################
def GetAuthor(str):
  return DeleteAfterSlash(str)

########################################
# 予約者数を取得
# str : 対象文字列
# RET : 予約者数
########################################
def GetReserve(str):
  return int(str)


if __name__ == '__main__':
  url = 'http://www.city.yokohama.lg.jp/kyoiku/library/yoyaku50.html'
  count = 0

  if len(sys.argv) != 2:
    sys.exit("usage : > python sqlite_CreateTable.py [DatabaseName]")
  db_path = sys.argv[1]
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  d = datetime.datetime.today()

  
  with GetPage(url) as page:
    for line in page.readlines():
      s = CheckLine(line)
      if s:
        if count % 4 == 0:            # 順位
          rank = GetRank(s)
        elif count % 4 == 1:          # タイトル
          title = GetTitle(s)
        elif count % 4 == 2:          # 著者
          author = GetAuthor(s)
        elif count % 4 == 3:          # 予約件数
          reserve = GetReserve(s)
          '''
          print(rank, end = ',')
          print(title, end = ',')
          print(author, end = ',')
          print(reserve)
          '''
          query = "insert into YokohamaLibraryTop50 values (\"" + d.strftime("%Y-%m-%d") + "\",\"" + str(rank) + "\",\"" + title + "\",\"" + author + "\",\"" + str(reserve) + "\")"
          try:
            c.execute(query)
            conn.commit()
          except:
            print("Error : ", end = '')
            print(query)
        count += 1
  c.close()