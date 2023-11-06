import pandas as pd
import sys


fields = ['id','uid',"prediction","created_at","url","title","datetime"]

nrows = 300000000000000000000
path = '/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_values_url_with_label_2.csv'
df_06to08=pd.read_csv(path, nrows=nrows).loc[:, fields]

path = '/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_T/concat/2021-09to10_values_url_with_label_2.csv'
df_09to10=pd.read_csv(path, nrows=nrows).loc[:, fields]

df = pd.concat([df_06to08, df_09to10])
df.to_pickle(sys.argv[1])
