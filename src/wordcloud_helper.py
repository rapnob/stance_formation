def mecab_origin(text, use_features, lemmatize=False, avoid_ancillary_verb=False):
    node = tagger.parseToNode(text)
    word=""
    while node:
        s = node.feature.split(",")
        hinshi = s[0]
        print(node.surface)
        print(node.feature)
        
        if hinshi in use_features:
            if lemmatize:
                n = s[-3]
                if n == '*':
                    n = node.surface
            else:
                n = node.surface
            if hinshi == '動詞' and avoid_ancillary_verb and s[1] != '自立':
                pass
            else:
                word = word + " " + n
        node = node.next
    return word


def chi_origin(class0,class1):
    word_list = list(set(set(class0.keys()) | set(class1.keys())))
    N_class0 = sum(class0.values())
    N_class1 = sum(class1.values())

    result=[]
    for word in word_list:
        data=[[class0[word], N_class0 - class0[word]], [class1[word], N_class1 - class1[word]]]

        bigger_class = 0 if class0[word] > class1[word] else 1
        size=class0[word] if class0[word] > class1[word] else class1[word]

        chi2, p, dof, ex = stats.chi2_contingency(data, correction=False)
        if p < 0.05:
            result.append((bigger_class, word, size))
    return result


def mecab_arr(text, tagger, use_features, lemmatize=False, avoid_ancillary_verb=False):
    text = unicodedata.normalize('NFC', text)
    node = tagger.parseToNode(text)
    words=[]
    while node:
        s = node.feature.split(",")
        hinshi = s[0]
        if len(use_features) == 0 or hinshi in use_features:
            if lemmatize:
                n = s[-3]
                if n == '*':
                    n = node.surface
            else:
                n = node.surface
            if hinshi == '動詞' and avoid_ancillary_verb and s[1] != '自立':
                pass
            else:
                words.append(n)
        node = node.next
    return words

def make_joined_tokens_per_user(urls_month, tagger, use_features, lemmatize=False, avoid_ancillary_verb=False):
    uid2tokens = collections.defaultdict(set)
    for title, _, uid in urls_month:
        tokens = mecab_arr(title, tagger, use_features=use_features, lemmatize=lemmatize, avoid_ancillary_verb=avoid_ancillary_verb)
        for token in tokens:
            uid2tokens[uid].add(token)
            # if token not in stopwords and len(token) > 1:
                # uid2tokens[uid].add(token)
    token2usernum = collections.Counter()
    for tokens in uid2tokens.values():
        for token in tokens:
            token2usernum[token] += 1
    arr = []
    for token, num in token2usernum.items():
        for _ in range(num):
            arr.append(token)
    joined_tokens = ' '.join(arr)
    return joined_tokens

def make_joined_tokens_origin(urls_month, lemmatize=False, use_features=["名詞","動詞","形容詞","形容動詞"], avoid_ancillary_verb=False):
    title=np.array(urls_month)[:, 0]
    title=[mecab_origin(x, use_features, lemmatize=lemmatize, avoid_ancillary_verb=avoid_ancillary_verb) for x in title]
    txt=' '.join(title)    
    return txt

stopwords_origin = set(["春彦","ã","0","1","2","3","4","１","４","２","０","３","回","TOCANA","ナショナル","ジオグラフィック","人間","日本","守る","ない","地球","地震","自然","ルイ","及川","邦彦","考える","気象","","4","21","20","24",":","コム","ドット","メンタリスト","DaiGo","Yahoo","!","|","ニュース","NHK","デイリースポーツ","ワクチン","コロナ","接種","新型","8","9","10","7","6","月","2021","日",'あそこ', 'あたり', 'あちら', 'あっち', 'あと', 'あな', 'あなた', 'あれ', 'いくつ', 'いつ', 'いま', 'いや', 'いろいろ', 'うち', 'おおまか', 'おまえ', 'おれ', 'がい', 'かく', 'かたち', 'かやの', 'から', 'がら', 'きた', 'くせ', 'ここ', 'こっち', 'こと', 'ごと', 'こちら', 'ごっちゃ', 'これ', 'これら', 'ごろ', 'さまざま', 'さらい', 'さん', 'しかた', 'しよう', 'すか', 'ずつ', 'すね', 'すべて', 'ぜんぶ', 'そう', 'そこ', 'そちら', 'そっち', 'そで', 'それ', 'それぞれ', 'それなり', 'たくさん', 'たち', 'たび', 'ため', 'だめ', 'ちゃ', 'ちゃん', 'てん', 'とおり', 'とき', 'どこ', 'どこか', 'ところ', 'どちら', 'どっか', 'どっち', 'どれ', 'なか', 'なかば', 'なに', 'など', 'なん', 'はじめ', 'はず', 'はるか', 'ひと', 'ひとつ', 'ふく', 'ぶり', 'べつ', 'へん', 'ぺん', 'ほう', 'ほか', 'まさ', 'まし', 'まとも', 'まま', 'みたい', 'みつ', 'みなさん', 'みんな', 'もと', 'もの', 'もん', 'やつ', 'よう', 'よそ', 'わけ', 'わたし', 'ハイ', '上', '中', '下', '字', '年', '月', '日', '時', '分', '秒', '週', '火', '水', '木', '金', '土', '国', '都', '道', '府', '県', '市', '区', '町', '村', '各', '第', '方', '何', '的', '度', '文', '者', '性', '体', '人', '他', '今', '部', '課', '係', '外', '類', '達', '気', '室', '口', '誰', '用', '界', '会', '首', '男', '女', '別', '話', '私', '屋', '店', '家', '場', '等', '見', '際', '観', '段', '略', '例', '系', '論', '形', '間', '地', '員', '線', '点', '書', '品', '力', '法', '感', '作', '元', '手', '数', '彼', '彼女', '子', '内', '楽', '喜', '怒', '哀', '輪', '頃', '化', '境', '俺', '奴', '高', '校', '婦', '伸', '紀', '誌', 'レ', '行', '列', '事', '士', '台', '集', '様', '所', '歴', '器', '名', '情', '連', '毎', '式', '簿', '匹', '個', '席', '束', '歳', '目', '通', '面', '円', '玉', '枚', '前', '後', '左', '右', '次', '先', '春', '夏', '秋', '冬', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '億', '兆', '下記', '上記', '時間', '今回', '前回', '場合', '一つ', '年生', '自分', 'ヶ所', 'ヵ所', 'カ所', '箇所', 'ヶ月', 'ヵ月', 'カ月', '箇月', '名前', '本当', '確か', '時点', '全部', '関係', '近く', '方法', '我々', '違い', '多く', '扱い', '新た', 'その後', '半ば', '結局', '様々', '以前', '以後', '以降', '未満', '以上', '以下', '幾つ', '毎日', '自体', '向こう', '何人', '手段', '同じ', '感じ','(',')','/','し','する','の','さ','#','るい','ネット','―','-','_','い','れ','いる','～','~','∼','￣','～'])
