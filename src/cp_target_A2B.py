
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_edges_pickle', type=str)
    parser.add_argument('input_A2B_pickle', type=str)
    parser.add_argument('output_cp_targets_toposi_before_pickle', type=str)
    parser.add_argument('--nrows', type=int, default=30000000000000000000000)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()


import pandas as pd
import datetime
import logging
from tqdm import tqdm


fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)

logging.info('Loading edges...')
edges = pd.read_pickle(args.input_edges_pickle)
logging.info('Loaded.')


A2B_dict = pd.read_pickle(args.input_A2B_pickle)
A2B_result_dict = dict()


for A2B in [(0, 0), (1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1)]:

    toposi = A2B_dict[A2B]
    cp_targets_toposi=[]

    alluids = set(x[0] for x in toposi)
    edges__ = edges[edges.source.isin(alluids)]
    edges__.loc[:, ['time']] = pd.to_datetime(edges__.time)
    td10d = datetime.timedelta(10)
    for id_,timestamp in tqdm(toposi, ncols=100, desc=f'{A2B[0]} to {A2B[1]}'):
        # edges_=edges[edges['source']==id_].copy()
        # edges_.loc[:,['time']]=pd.to_datetime(edges_['time'])
        edges_=edges__[edges__['source']==id_].loc[:, ['time', 'target', 'type']]
        targets=edges_[(edges_['time']>=timestamp-td10d)&(edges_['time']<timestamp+td10d)].loc[:,['target','type']].values.tolist()
        cp_targets_toposi.extend([x for x in targets if x[0]!='-'])
    A2B_result_dict[A2B] = cp_targets_toposi

pd.to_pickle(A2B_result_dict, args.output_cp_targets_toposi_before_pickle)
logging.info('Finished.')
