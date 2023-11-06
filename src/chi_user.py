import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_targets_toposi_pickle', type=str)
    parser.add_argument('input_cp_targets_tonega_pickle', type=str)
    parser.add_argument('output_attribute_pickle', type=str)
    parser.add_argument("--log", default="WARNING")
    parser.add_argument("--nrows", default=3000000000000000000, type=int)
    return parser.parse_args()

args = parse_arguments()
nrows = args.nrows

import pandas as pd
import logging
import collections
import pickle

from tqdm import tqdm
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=args.log, format=fmt)

from UserAttributeCollector import UserAttributeCollector
from chi import chi2

logging.info('Start')


uac=UserAttributeCollector()



cp_targets_toposi = pd.read_pickle(args.input_cp_targets_toposi_pickle)
cp_targets_tonega = pd.read_pickle(args.input_cp_targets_tonega_pickle)

df_tmp_nega=pd.DataFrame(cp_targets_tonega,columns=['target','type'])
df_tmp_posi=pd.DataFrame(cp_targets_toposi,columns=['target','type'])


ls_=collections.Counter(df_tmp_posi['target'].to_list())
ls_not=collections.Counter(list(collections.Counter(df_tmp_nega['target'].to_list())))

result = chi2(ls_,ls_not,0.05)

words_dict={}
for r in result:
    if r[0]==0:
        words_dict[r[1]]=r[2]

ls_posi=list(collections.Counter(words_dict).most_common(30))
attribute=[]

logging.info('Loading raw data...')
path = f'/data/str01_03/twitter/hisamits/data/youtube/2021-06to08_T/concat/2021-06to08_all_with_label_not_just_share_2.csv'
df = pd.read_csv(path, nrows=nrows)
logging.info('Loaded.')


no_desc_usr_num = 0
for i, l in enumerate(ls_posi):
    aa = df[df['uid']==l[0]]
    bb = aa['user/description'].to_list()
    if len(bb) > 0:
        jobs = uac.find_match(bb[0])
    else:
        # RTだけする人（ツイート無い人）
        jobs = uac.find_match('')
        no_desc_usr_num += 1
    attribute.append(jobs)

with open(args.output_attribute_pickle, 'wb') as f:
    pickle.dump(collections.Counter([x[2] for x in attribute]), f)

print('no description info user: ' + str(no_desc_usr_num))
logging.info('Finished.')
