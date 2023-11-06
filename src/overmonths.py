import pickle, collections
import numpy as np
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_urls_toposi_before_pickle', type=str)
    parser.add_argument('output_overmonths_posi_pickle', type=str)
    return parser.parse_args()

args = parse_arguments()


p = "data/cp_urls_toposi_before.pickle"
p = args.input_cp_urls_toposi_before_pickle
with open(p, "rb") as f:
    cp_urls_toposi_before = pickle.load(f)

over_monthes=[]
for i in range(len(cp_urls_toposi_before)):
    urls_month=cp_urls_toposi_before[i]
    if len(urls_month) > 0:
        cnt = collections.Counter(np.unique(np.array(urls_month)[:,[1,2]],axis=0)[:,0])
        over_monthes.append(np.array(cnt.most_common(20))[:,0])
    else:
        over_monthes.append([])
        
p = "data/overmonths_posi.pickle"
p = args.output_overmonths_posi_pickle
with open(p, "wb") as f:
    pickle.dump(over_monthes, f)
