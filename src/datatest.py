import pandas as pd
import argparse

import collections, pickle
from datetime import datetime
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_file_path', type=str)
    parser.add_argument('output_unique_users_pickle', type=str)
    parser.add_argument('output_time_series_counter_pickle', type=str)
    parser.add_argument('output_time_series_counter_old_pickle', type=str)
    parser.add_argument('output_time_series_counter_old2_pickle', type=str)
    parser.add_argument('--nrows', type=int, default=30000000000000000000000)
    return parser.parse_args()

args = parse_arguments()
nrows = args.nrows

fields = ['uid',"prediction","created_at"]

path = args.input_file_path
# df = pd.read_pickle('../../covid/ASONAM2022_journal/data/alldf.pickle')


if path.endswith('.pickle'):
    df = pd.read_pickle(path)
elif path.endswith('hisa'):

    path = '/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_all_with_label_not_just_share_2.csv'
    df_06to08=pd.read_csv(path, nrows=nrows).loc[:, fields]
    # df_06to08=df_06to08[df_06to08['uid'].isin(selected_users.keys())]

    path = '/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_T/concat/2021-09to10_all_with_label_not_just_share_2.csv'
    df_09to10=pd.read_csv(path, nrows=nrows).loc[:, fields]
    # df_09to10=df_09to10[df_09to10['uid'].isin(selected_users.keys())]

    df=pd.concat([df_06to08, df_09to10])

    del df_06to08
    del df_09to10
    
elif path.endswith('.csv'):
    df = pd.read_csv(path, nrows=args.nrows)
elif path.endswith('.tsv'):
    df = pd.read_csv(path, nrows=args.nrows, sep='\t')
else:
    raise ValueError('Invalid file format.')

unique_users=df.set_index('uid').loc[:,['prediction']].groupby(level=0).count()
labels = df.set_index('uid')['prediction'].to_list()
created_at = []

for x in tqdm(df['created_at'].to_list()):
    dt = datetime.strptime('-'.join(x.split(' ')[1:3]),"%b-%d").replace(year=2021)
    created_at.append(dt)



time_series_counter = collections.Counter()
time_series_counter_old = collections.Counter()
time_series_counter_old2 = collections.Counter()
u_ids = df.uid.values

# for i in tqdm(range(len(labels))):
#     stance = labels[i]
#     if stance>0:
#         time_series_counter[(u_ids[i],created_at[i],"1")]+=1
#         time_series_counter_old[(u_ids[i],created_at[i])]+=1
#     elif stance<0:
#         time_series_counter[(u_ids[i],created_at[i],"-1")]+=1
#         time_series_counter_old[(u_ids[i],created_at[i])]-=1
#     else:
#         time_series_counter[(u_ids[i],created_at[i],"0")]+=1
#         time_series_counter_old[(u_ids[i],created_at[i])]+=1
#         time_series_counter_old[(u_ids[i],created_at[i])]-=1

for i in tqdm(range(len(labels))):
    stance = labels[i]
    if stance>0:
        time_series_counter[(u_ids[i],created_at[i],"1")]+=1
        time_series_counter_old [(u_ids[i],created_at[i])]+=1
        time_series_counter_old2[(u_ids[i],created_at[i])]+=1
    elif stance<0:
        time_series_counter[(u_ids[i],created_at[i],"-1")]+=1
        time_series_counter_old [(u_ids[i],created_at[i])]-=1
        time_series_counter_old2[(u_ids[i],created_at[i])]-=1
    else:
        time_series_counter[(u_ids[i],created_at[i],"0")]+=1
        time_series_counter_old2[(u_ids[i],created_at[i])]+=1
        time_series_counter_old2[(u_ids[i],created_at[i])]-=1

p = "data/unique_users.pickle"
p = args.output_unique_users_pickle

with open(p, "wb") as f:
    pickle.dump(unique_users, f)


p = "data/time_series_counter.pickle"
p = args.output_time_series_counter_pickle
with open(p, "wb") as f:
    pickle.dump(time_series_counter, f)

    

p = "data/time_series_counter_old.pickle"
p = args.output_time_series_counter_old_pickle
with open(p, "wb") as f:
    pickle.dump(time_series_counter_old, f)


p = "data/time_series_counter_old2.pickle"
p = args.output_time_series_counter_old2_pickle
with open(p, "wb") as f:
    pickle.dump(time_series_counter_old2, f)
