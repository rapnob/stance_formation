import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_selected_users', type=str)
    parser.add_argument('output_edges', type=str)
    parser.add_argument("--log", default="WARNING")
    parser.add_argument("--nrows", default=300000000000000000, type=int)
    return parser.parse_args()

args = parse_arguments()


import pandas as pd
import logging
from tqdm import tqdm


fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=args.log, format=fmt)

path = args.input_selected_users
selected_users = pd.read_pickle(path)
nrows = args.nrows
edges=pd.read_csv("/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_RMQ_tlg/edges/2021-06-1-10_edges.csv", nrows=nrows)
spans=["06-11-20","06-21-30","07-1-10","07-11-20","07-21-31","08-1-10","08-11-20","08-21-31","09-1-10","09-11-20","09-21-30","10-1-10","10-11-20","10-21-31"]
# spans=["06-11-20"]
c=0
logging.info('Loading edges...')
for span in tqdm(spans):

    m=span.split('-')[0]
    s=span.split('-')[1]
    e=span.split('-')[2]
    start=pd.to_datetime('2021-'+m+'-'+s)
    end=pd.to_datetime('2021-'+m+'-'+e)
    if m in ['06','07','08']:
        dir_="2021-06to08_RMQ_tlg"
    else:
        dir_="2021-09to10_RMQ_tlg"
    edges_sep = pd.read_csv("/data/str01_03/twitter/hisamits/data/youtube/"+dir_+"/edges/2021-"+span+"_edges.csv", nrows=nrows)
    edges_sep=edges_sep[edges_sep['source'].isin(selected_users.keys())].copy()
    edges=pd.concat([edges,edges_sep], join='outer').reset_index(drop=True)
    
logging.info('Writing edges...')
    
pd.to_pickle(edges, args.output_edges)
logging.info('Finished.')
