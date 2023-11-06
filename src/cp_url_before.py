import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('input_file_path', type=str)
    parser.add_argument('input_toposi_pickle', type=str)
    parser.add_argument('start_stance', type=int)
    parser.add_argument('end_stance', type=int)
    parser.add_argument('output_cp_urls_toposi_before_pickle', type=str)
    parser.add_argument('--nrows', type=int, default=30000000000000000000000)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()


import pandas as pd
import datetime as dt
import collections
import pickle
import logging
from urllib.parse import urlparse
from tqdm import tqdm
from datetime import datetime


fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)

path = args.input_file_path
nrows = args.nrows
# df = pd.read_pickle('../../covid/ASONAM2022_journal/data/alldf.pickle')


logging.info('Loading data...')
if path.endswith('.pickle'):
    df = pd.read_pickle(path)
elif path.endswith('.csv'):
    df = pd.read_csv(path, nrows=args.nrows)
elif path.endswith('hisa'):
    fields = ['uid',"url","title","datetime"]

    path = '/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_all_with_label_not_just_share_2.csv'
    df_06to08=pd.read_csv(path, nrows=nrows).loc[:, fields]
    # df_06to08=df_06to08[df_06to08['uid'].isin(selected_users.keys())]

    path = '/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_T/concat/2021-09to10_all_with_label_not_just_share_2.csv'
    df_09to10=pd.read_csv(path, nrows=nrows).loc[:, fields]
    # df_09to10=df_09to10[df_09to10['uid'].isin(selected_users.keys())]

    df=pd.concat([df_06to08, df_09to10])

    del df_06to08
    del df_09to10
    
elif path.endswith('.tsv'):
    df = pd.read_csv(path, nrows=args.nrows, sep='\t')
else:
    raise ValueError('Invalid file format.')

logging.info('Finished.')

p = "data/toposi.pickle"
p = args.input_toposi_pickle
with open(p, "rb") as f:
    A2B_dict = pickle.load(f)
A2B = (args.start_stance, args.end_stance)

toposi = A2B_dict[A2B]

cp_urls_toposi_before=[]
dates=["2021/6/1","2021/7/1","2021/8/1","2021/9/1","2021/10/1","2021/10/31"]
alluids = set(x[0] for x in toposi)
df__ = df[df['uid'].isin(alluids)]
td10d = dt.timedelta(10)
df__.loc[:, ['datetime_dt']] = pd.to_datetime(df__['datetime'])

for i in tqdm(range(len(dates)-1)):
    l=[]
    for id_, timestamp in toposi:
        if pd.to_datetime(dates[i]) < timestamp < pd.to_datetime(dates[i+1]):
            # 対象とする変容ユーザの投稿のみを抽出
            df_=df__[df__['uid']==id_].copy()

            # 変容前後10日間のリンクシェアを抽出
            urls=df_[(df_['datetime_dt']>=timestamp-td10d)&(df_['datetime_dt']<timestamp+td10d)].loc[:,['title','url','uid']].values.tolist()

            # 記録
            l.extend([[
                x[0],
                '{uri.netloc}'.format(uri=urlparse(x[1]))
                ,x[2]
            ] for x in urls if x[0]!='-'])

    cp_urls_toposi_before.append(l)


p = "data/cp_urls_toposi_before.pickle"
p = args.output_cp_urls_toposi_before_pickle
with open(p, "wb") as f:
    pickle.dump(cp_urls_toposi_before, f)
