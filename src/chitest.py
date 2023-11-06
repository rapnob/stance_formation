

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_targets_A2B_before_overtime_pickle', type=str)
    parser.add_argument('output_chi_result_overtime_pickle', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

from scipy import stats
def chi2_all(class0, class1):
    word_list = list(set(set(class0.keys()) | set(class1.keys())))
    N_class0 = sum(class0.values())
    N_class1 = sum(class1.values())

    result=[]
    for word in word_list:
        data=[[class0[word], N_class0 - class0[word]], [class1[word], N_class1 - class1[word]]]

        bigger_class = 0 if class0[word] > class1[word] else 1
        size=class0[word] if class0[word] > class1[word] else class1[word]

        chi2, p_, dof, ex = stats.chi2_contingency(data, correction=False)
        result.append((bigger_class, word, size, p_))
    return result


from tqdm import tqdm

import pandas as pd
import collections

n2p = pd.read_pickle(args.n2p)
n2a = pd.read_pickle(args.n2a)

linkshare_n2p=collections.Counter(n2p)
linkshare_n2a=collections.Counter(n2a)

result = chi2_all(linkshare_n2p, linkshare_n2p)
