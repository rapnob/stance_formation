import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('output', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import pandas as pd
import logging

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)

logging.info('Loading hisa raw data1...')

path = f'/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_all_with_label_not_just_share_2.csv'
df1 = pd.read_csv(path, nrows=3000000000000).loc[:, ['uid', 'user/description']].drop_duplicates()

logging.info('Loading hisa raw data2...')

path = f'/data/str01_03/twitter/hisamits/data/youtube/2021-09to10_T/concat/2021-09to10_all_with_label_not_just_share_2.csv'
df2 = pd.read_csv(path, nrows=3000000000000).loc[:, ['uid', 'user/description']].drop_duplicates()

logging.info('Concatenationg data1 and data2...')

df = pd.concat([df1, df2])

logging.info('Writing concat data...')
pd.to_pickle(df, args.output)
logging.info('Finished.')
