import pickle
import pandas as pd
import argparse
import logging


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('hisadf_pickle', type=str)
    parser.add_argument('csdf_pickle', type=str)
    parser.add_argument('output_pickle', type=str)
    parser.add_argument("--log", default="WARNING")

    return parser.parse_args()

args = parse_arguments()



fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=args.log, format=fmt)

logging.info('Loading hisa data...')


# 久光らが使用したデータと同じデータを読み込み
fields = ['id', 'uid',"prediction","created_at","url","title","datetime"]

nrows = 300000000000000000000
path = '/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_all_with_label_not_just_share_2.csv'
df_06to08=pd.read_csv(path, nrows=nrows).loc[:, fields]

path = '/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_T/concat/2021-09to10_all_with_label_not_just_share_2.csv'
df_09to10=pd.read_csv(path, nrows=nrows).loc[:, fields]

df = pd.concat([df_06to08, df_09to10])

# csの再推定したスタンスデータ読み込み
p = 'data/cs/raw/cs.pickle'
logging.info('Loading cs data...')
p = args.csdf_pickle
with open(p, 'rb') as f:
    csdf = pickle.load(f)



# 久光らが使用したデータにcsスタンスラベルを付与
logging.info('Merging hisa data with cs data...')

fields2 = ['id', 'uid',"created_at","url","title","datetime"]
m = df.loc[:, fields2].merge(csdf.loc[:, ['id', 'prediction']], on='id')


# 出力
p = 'data/cs/raw/input.pickle'
p = args.output_pickle
logging.info('Writing merged data...')

with open(p, 'wb') as f:
    pickle.dump(m, f)

logging.info('Finished.')
