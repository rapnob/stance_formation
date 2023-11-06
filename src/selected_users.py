import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_unique_users_pickle', type=str)
    parser.add_argument('input_time_series_counter_pickle', type=str)
    parser.add_argument('output_selected_users_pickle', type=str)
    parser.add_argument('--nrows', type=int, default=30000000000000000000000)
    parser.add_argument('--config')
    parser.add_argument("--log", default="WARNING")
    return parser.parse_args()

args = parse_arguments()

import pandas as pd
import pickle, sys, json, logging
import numpy as np
from tqdm import tqdm

fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=args.log, format=fmt)


config = {'bugfix10d': False}
if args.config is not None:
    config = json.load(open(args.config, 'rb'))

    
date_indice = []
start="2021-06-01"
for i in range(15):
    date_index=pd.date_range(start=start, periods=10, freq="D")
    date_indice.append(date_index)
    start=str(date_index[-1])

def constant_post(id_, time_series_counter):
    stance=[]
    #starts=["2021-06-01","2021-07-01","2021-08-01","2021-09-01","2021-10-01"]
    #ends=["2021-06-30","2021-07-31","2021-08-31","2021-09-30","2021-10-31"]
    start="2021-06-01"
    #for start,end in zip(starts,ends):
    for i in range(15):
        #date_index=pd.date_range(start=start, end=end, freq="D")
        # date_index=pd.date_range(start=start, periods=10, freq="D")
        date_index=date_indice[i]
        start=str(date_index[-1])
        posi=0
        neu=0
        nega=0
        no_tweet=0
        for date in date_index:
            posi+=time_series_counter[(id_,date, "1")]
            neu +=time_series_counter[(id_,date, "0")]
            nega+=time_series_counter[(id_,date,"-1")]
        if max([posi,neu,nega])==0:
            if i==0:
                return False
            else:
                stance.append(stance[-1])
                no_tweet+=1
        else:
            m=np.argmax([posi,neu,nega])
            if m==0:
                stance.append(1)
            elif m==1:
                stance.append(0)
            else:
                stance.append(-1)
    if no_tweet<6:
        return stance
    else:
        return False


    
terms = [
    list(pd.date_range(start='2021-06-01', end='2021-06-10')),
    list(pd.date_range(start='2021-06-11', end='2021-06-20')),
    list(pd.date_range(start='2021-06-21', end='2021-06-30')),

    list(pd.date_range(start='2021-07-01', end='2021-07-10')),
    list(pd.date_range(start='2021-07-11', end='2021-07-20')),
    list(pd.date_range(start='2021-07-21', end='2021-07-31')),

    list(pd.date_range(start='2021-08-01', end='2021-08-10')),
    list(pd.date_range(start='2021-08-11', end='2021-08-20')),
    list(pd.date_range(start='2021-08-21', end='2021-08-31')),

    list(pd.date_range(start='2021-09-01', end='2021-09-10')),
    list(pd.date_range(start='2021-09-11', end='2021-09-20')),
    list(pd.date_range(start='2021-09-21', end='2021-09-30')),

    list(pd.date_range(start='2021-10-01', end='2021-10-10')),
    list(pd.date_range(start='2021-10-11', end='2021-10-20')),
    list(pd.date_range(start='2021-10-21', end='2021-10-31')),
]

terms_str = [[str(dateinfo).split(' ')[0] for dateinfo in term] for term in terms]

def constant_post_10dbugfix(id_, time_series_counter):
    stance=[]
    for i in range(15):
        posi=0
        neu=0
        nega=0
        no_tweet=0
        for date in terms[i]:
            posi+=time_series_counter[(id_,date, "1")]
            neu +=time_series_counter[(id_,date, "0")]
            nega+=time_series_counter[(id_,date,"-1")]
        if max([posi,neu,nega])==0:
            if i==0:
                return False
            else:
                stance.append(stance[-1])
                no_tweet+=1
        else:
            # print(posi, neu, nega)
            m=np.argmax([posi,neu,nega])
            if m==0:
                stance.append(1)
            elif m==1:
                stance.append(0)
            else:
                stance.append(-1)
    if no_tweet<6:
        return stance
    else:
        return False        

p = "data/unique_users.pickle"
p = args.input_unique_users_pickle
with open(p, "rb") as f:
    unique_users = pickle.load(f)

p = "data/time_series_counter.pickle"
p = args.input_time_series_counter_pickle
with open(p, "rb") as f:
    time_series_counter = pickle.load(f)

selected_users={}

if config['bugfix10d']:
    get_stance_arr_func = constant_post_10dbugfix
else:
    get_stance_arr_func = constant_post
    
for id_ in tqdm(list(set(unique_users.index))):
    d=get_stance_arr_func(id_, time_series_counter)
    if(d!=False):
        selected_users[id_]=d
        
p = "data/selected_users.pickle",

p = args.output_selected_users_pickle
with open(p, "wb") as f:
    pickle.dump(selected_users, f)
