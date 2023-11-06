
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
import collections
from tqdm import tqdm

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)

logging.info('Loading edges...')
edges = pd.read_pickle(args.input_edges_pickle)
logging.info('Loaded.')


A2B_dict = pd.read_pickle(args.input_A2B_pickle)
A2B_result_dict = collections.defaultdict(dict)

dates=["2021/6/1","2021/7/1","2021/8/1","2021/9/1","2021/10/1","2021/10/31"]
dates_dt = [pd.to_datetime(dt) for dt in dates]


for A2B in tqdm([(0, 0), (1, 1), (-1, -1), (0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1)]):
    toposi = A2B_dict[A2B]

    alluids = set(x[0] for x in toposi)
    logging.info(f'{A2B[0]: } to {A2B[1]: }: {len(toposi)} users')
    logging.info(f'{A2B[0]: } to {A2B[1]: }: {len(alluids)} users')
    edges__ = edges[edges.source.isin(alluids)]
    edges__.loc[:, ['time']] = pd.to_datetime(edges__.time)
    td10d = datetime.timedelta(10)
    for date_idx in range(len(dates_dt)-1):
        cp_targets_toposi=[]
        if A2B[0] == A2B[1]:
            edges_in_month = edges__[(edges__['time']>=dates_dt[date_idx])&(edges__['time']<dates_dt[date_idx+1])]
            # ずっと同じスタンスのユーザ
            for id_,timestamp in (toposi):
                # edges_=edges__[edges__['source']==id_].copy()
                # targets=edges_[(edges_['time']>=dates_dt[date_idx])&(edges_['time']<dates_dt[date_idx+1])].loc[:,['target','type']].values.tolist()
                targets=edges_in_month[edges_in_month['source']==id_].loc[:, ['target', 'type']].values.tolist()
                cp_targets_toposi.extend([x for x in targets if x[0]!='-'])
        else:
            for id_,timestamp in (toposi):
                if dates_dt[date_idx] < timestamp < dates_dt[date_idx+1]:
                    # edges_=edges__[edges__['source']==id_].copy()
                    # targets=edges_[(edges_['time']>=timestamp-td10d)&(edges_['time']<timestamp+td10d)].loc[:,['target','type']].values.tolist()
                    
                    edges_=edges__[edges__['source']==id_].loc[:, ['time', 'target', 'type']].copy()
                    targets=edges_[(edges_['time']>=timestamp-td10d)&(edges_['time']<timestamp+td10d)].loc[:, ['target','type']].values.tolist()
                    
                    cp_targets_toposi.extend([x for x in targets if x[0]!='-'])
        A2B_result_dict[A2B][date_idx] = cp_targets_toposi

pd.to_pickle(A2B_result_dict, args.output_cp_targets_toposi_before_pickle)
logging.info('Finished.')
