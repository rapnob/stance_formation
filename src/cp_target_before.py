
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('input_edges_pickle', type=str)
    parser.add_argument('input_A2B_pickle', type=str)
    parser.add_argument('start_stance', type=int)
    parser.add_argument('end_stance', type=int)
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

A2B_dict = pd.read_pickle(args.input_A2B_pickle)
A2B = (args.start_stance, args.end_stance)
n2p = A2B_dict[A2B]

logging.info('Loading edges...')
edges = pd.read_pickle(args.input_edges_pickle)
logging.info('Loaded.')
toposi = n2p


cp_targets_toposi=[]

alluids = set(x[0] for x in toposi)
edges__ = edges[edges.source.isin(alluids)]
edges__.loc[:, ['time_dt']] = pd.to_datetime(edges__.time)
td10d = datetime.timedelta(10)
for id_,timestamp in tqdm(toposi, desc=f'Extracting users shred by {A2B[0]} to {A2B[1]}'):
    edges_=edges__[edges__['source']==id_].copy()
    targets=edges_[(edges_['time_dt']>=timestamp-td10d)&(edges_['time_dt']<timestamp+td10d)].loc[:,['target','type']].values.tolist()
    cp_targets_toposi.extend([x for x in targets if x[0]!='-'])

pd.to_pickle(cp_targets_toposi, args.output_cp_targets_toposi_before_pickle)

logging.info('Finished.')
