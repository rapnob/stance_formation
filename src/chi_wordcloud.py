import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_urls_n2p_before', type=str)
    parser.add_argument('input_cp_urls_n2a_before', type=str)
    parser.add_argument('output_chi_result_wordcloud', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import logging
from tqdm import tqdm

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)



import pandas as pd
import numpy as np

import MeCab
import pickle
import collections
import unicodedata
import re

from scipy import stats
from tqdm import tqdm

pat_num = re.compile('^\d+$')


path="-r /home/cs/usr/rsc/mecabrc -d /home/hisamits/centos7/lib/mecab/dic/ipadic"
# path="/home/hisamits/src/mecab-ipadic-neologd -r /home/cs/usr/rsc/mecabrc "
tagger_ipa = MeCab.Tagger(path)

path="-r /home/cs/usr/rsc/mecabrc -d /home/hisamits/centos7/lib/mecab/dic/mecab-ipadic-neologd/"
tagger_neologd = MeCab.Tagger(path)

cp_urls_n2p_before = pickle.load(open(args.cp_urls_n2p_before, 'rb'))
cp_urls_n2a_before = pickle.load(open(args.cp_urls_n2a_before, 'rb'))

stopwords_origin = {"春彦","ã","0","1","2","3","4","１","４","２","０","３","回","TOCANA","ナショナル","ジオグラフィック","人間","日本","守る","ない","地球","地震","自然","ルイ","及川","邦彦","考える","気象","","4","21","20","24",":","コム","ドット","メンタリスト","DaiGo","Yahoo","!","|","ニュース","NHK","デイリースポーツ","ワクチン","コロナ","接種","新型","8","9","10","7","6","月","2021","日",'あそこ', 'あたり', 'あちら', 'あっち', 'あと', 'あな', 'あなた', 'あれ', 'いくつ', 'いつ', 'いま', 'いや', 'いろいろ', 'うち', 'おおまか', 'おまえ', 'おれ', 'がい', 'かく', 'かたち', 'かやの', 'から', 'がら', 'きた', 'くせ', 'ここ', 'こっち', 'こと', 'ごと', 'こちら', 'ごっちゃ', 'これ', 'これら', 'ごろ', 'さまざま', 'さらい', 'さん', 'しかた', 'しよう', 'すか', 'ずつ', 'すね', 'すべて', 'ぜんぶ', 'そう', 'そこ', 'そちら', 'そっち', 'そで', 'それ', 'それぞれ', 'それなり', 'たくさん', 'たち', 'たび', 'ため', 'だめ', 'ちゃ', 'ちゃん', 'てん', 'とおり', 'とき', 'どこ', 'どこか', 'ところ', 'どちら', 'どっか', 'どっち', 'どれ', 'なか', 'なかば', 'なに', 'など', 'なん', 'はじめ', 'はず', 'はるか', 'ひと', 'ひとつ', 'ふく', 'ぶり', 'べつ', 'へん', 'ぺん', 'ほう', 'ほか', 'まさ', 'まし', 'まとも', 'まま', 'みたい', 'みつ', 'みなさん', 'みんな', 'もと', 'もの', 'もん', 'やつ', 'よう', 'よそ', 'わけ', 'わたし', 'ハイ', '上', '中', '下', '字', '年', '月', '日', '時', '分', '秒', '週', '火', '水', '木', '金', '土', '国', '都', '道', '府', '県', '市', '区', '町', '村', '各', '第', '方', '何', '的', '度', '文', '者', '性', '体', '人', '他', '今', '部', '課', '係', '外', '類', '達', '気', '室', '口', '誰', '用', '界', '会', '首', '男', '女', '別', '話', '私', '屋', '店', '家', '場', '等', '見', '際', '観', '段', '略', '例', '系', '論', '形', '間', '地', '員', '線', '点', '書', '品', '力', '法', '感', '作', '元', '手', '数', '彼', '彼女', '子', '内', '楽', '喜', '怒', '哀', '輪', '頃', '化', '境', '俺', '奴', '高', '校', '婦', '伸', '紀', '誌', 'レ', '行', '列', '事', '士', '台', '集', '様', '所', '歴', '器', '名', '情', '連', '毎', '式', '簿', '匹', '個', '席', '束', '歳', '目', '通', '面', '円', '玉', '枚', '前', '後', '左', '右', '次', '先', '春', '夏', '秋', '冬', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '億', '兆', '下記', '上記', '時間', '今回', '前回', '場合', '一つ', '年生', '自分', 'ヶ所', 'ヵ所', 'カ所', '箇所', 'ヶ月', 'ヵ月', 'カ月', '箇月', '名前', '本当', '確か', '時点', '全部', '関係', '近く', '方法', '我々', '違い', '多く', '扱い', '新た', 'その後', '半ば', '結局', '様々', '以前', '以後', '以降', '未満', '以上', '以下', '幾つ', '毎日', '自体', '向こう', '何人', '手段', '同じ', '感じ','(',')','/','し','する','の','さ','#','るい','ネット','―','-','_','い','れ','いる','～','~','∼','￣','～'}