import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_selected_users_pickle', type=str)
    parser.add_argument('output_A2B_pickle', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import datetime as dt
import pandas as pd
import pickle
import logging
import collections

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)


def changed_only_once(l):
    state=l[0]
    c=0
    cp=0
    for i in range(1,len(l)):
        if l[i]!=state:
            c+=1
            state=l[i]
            cp=i
    if c>1:
        return -1
    else:
        return cp



p = "data/selected_users.pickle"
p = args.input_selected_users_pickle
with open(p, "rb") as f:
    selected_users = pickle.load(f)

A2B=collections.defaultdict(list)
n2p=[]
n2a=[]
n2n=[]
p2n=[]
p2a=[]
p2p=[]
a2p=[]
a2n=[]
a2a=[]

start=pd.to_datetime("2021-06-01")
logging.info('Start XXX...')
for key, value in zip(selected_users.keys(),selected_users.values()):
    cp=changed_only_once(value)
    if cp>=0:
        start_stance, last_stance = value[0], value[-1]
        # start_stance == last_stanceの場合はスタンス変化日として2021-6-1を登録する
        spair = (start_stance, last_stance)
        entry = [key, start + pd.Timedelta(10*cp,"d")]
        if spair == (0, 1):
            n2p.append(entry)
        elif spair == (0, -1):
            n2a.append(entry)
        elif spair == (0, 0):
            n2n.append(entry)
        elif spair == (1, 0):
            p2n.append(entry)
        elif spair == (1, -1):
            p2a.append(entry)
        elif spair == (1, 1):
            p2p.append(entry)
        elif spair == (-1, 0):
            a2n.append(entry)
        elif spair == (-1, 1):
            a2p.append(entry)
        elif spair == (-1, -1):
            a2a.append(entry)
        else:
            raise ValueError(f'Error: key: {key}, value: {value}\n')

A2B[( 0,  0)] = n2n
A2B[( 0,  1)] = n2p
A2B[( 0, -1)] = n2a
A2B[( 1,  0)] = p2n
A2B[( 1, -1)] = p2a
A2B[( 1,  1)] = p2p
A2B[(-1,  0)] = a2n
A2B[(-1, -1)] = a2a
A2B[(-1,  1)] = a2p

p = args.output_A2B_pickle
with open(p, "wb") as f:
    pickle.dump(A2B, f)
logging.info('Finished.')
