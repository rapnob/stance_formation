import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('span', type=str, choices=['06to08', '09to10'])
    parser.add_argument('output', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import logging
import json, glob, pickle
from tqdm import tqdm
fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)

logging.info('Start...')
span = args.span



uid2desc = dict()

if span == '06to08':
    
    for path in tqdm(glob.glob(f'/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_RMQ/*.json')):
        for line in open(path, 'rb'):
            d = json.loads(line)
            ud = d['user']
            uid2desc[int(ud['id_str'])] = ud['description']
elif span == '09to10':        
    for path in tqdm(glob.glob(f'/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_RMQ/*.json')):
        for line in open(path, 'rb'):
            d = json.loads(line)
            ud = d['user']
            uid2desc[int(ud['id_str'])] = ud['description']

    logging.info('Writing concat data...')
with open(args.output, 'wb') as f:
    pickle.dump(uid2desc, f)
logging.info('Finished.')
