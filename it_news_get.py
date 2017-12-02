# coding: utf-8

'''
【WebScraping サンプルソース】
  テクノプロ･IT社サイトの新着情報を取得する。（日付、内容、ＵＲＬ）
  取得した情報をコンソール画面に出力し、jsonファイルを作成する。
'''

import requests
from bs4 import BeautifulSoup
import json
import time

# 外部から実行されても負荷を与えないように1秒待つ
time.sleep(1)

#テクノプロ･IT社の新着情報サイトを設定
geturl = 'http://www.technopro.com/it/category/news/'

# HTMLを取得
response = requests.get(geturl)
response.encoding = 'utf-8'

# BeautifulSoupを用いて取得したHTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')

# HTMLに書かれたdtタグのテキスト情報を取得（新着情報の日付）
ldate = [a_tag.string for a_tag in soup.find_all('dt')]  # ←内包表記

# HTMLに書かれたaタグのテキストとリンク情報を取得（新着情報の内容とリンク）
ldesc = [a_tag.string for a_tag in soup.find_all('a') if a_tag.string != None and ('release' in a_tag.get('href') or '%' in a_tag.get('href'))]  # ←内包表記
lurl = [a_tag.get('href') for a_tag in soup.find_all('a') if a_tag.string != None and ('release' in a_tag.get('href') or '%' in a_tag.get('href'))]  # ←内包表記

# 取得した情報をjson用に辞書化する
jwrite = [{'date': a, 'desc': b, 'url': c} for a, b, c in zip(ldate, ldesc, lurl)]  # ←内包表記

# 画面出力（文字列の形成は書式指定で行う）
console = lambda pdate, pdesc, purl: '{} : {} <{}>'.format(p[pdate], p[pdesc], p[purl])  # ←無駄にラムダ式を使ってみた
for p in jwrite:
    print(console('date', 'desc', 'url'))

# json書き込み
with open('it_news.json', 'w', encoding='utf-8') as f:
    json.dump(jwrite, f, ensure_ascii=False, indent=2)
