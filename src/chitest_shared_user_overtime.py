

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_targets_A2B_before_overtime_pickle', type=str)
    parser.add_argument('output_chi_result_overtime_pickle', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import logging
from tqdm import tqdm

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)


import pandas as pd
from chi import chi2_all
import collections


configs = []
config = dict()

# posi vs (nega&neutral)にするならTrue, posi vs negaにするならFalse
for chi_with_neutral in [True, False]:

    # ls_not (A vs BのB）の実装を久光準拠にするならTrue
    for follow_hisa_impl in [True, False]:
        config['chi_with_neutral'] = chi_with_neutral
        config['follow_hisa_impl'] = follow_hisa_impl
        configs.append(config.copy())
        config.clear()


A2B_overtime2 = pd.read_pickle(args.input_cp_targets_A2B_before_overtime_pickle)

df_dict = {
    'posi': [pd.DataFrame(A2B_overtime2[( 0,  1)][month_i],columns=['target','type']) for month_i in range(5)],
    'nega': [pd.DataFrame(A2B_overtime2[( 0, -1)][month_i],columns=['target','type']) for month_i in range(5)],
    'neut': [pd.DataFrame(A2B_overtime2[( 0,  0)][month_i],columns=['target','type']) for month_i in range(5)],
}


records = []

for config_idx, config in tqdm(enumerate(configs), total=len(configs), desc='Using all configs...'):
    chi_with_neutral = config['chi_with_neutral']
    follow_hisa_impl = config['follow_hisa_impl']
    results = {
        'posi': [],
        'nega': [],
    }


    for month_i in tqdm(range(5)):
        record = []
        for posneg in ['posi', 'nega']:
            negpos = 'nega'
            if posneg == 'nega':
                negpos = 'posi'
            df_tmp_dict = {
                'posi': df_dict['posi'][month_i],
                'nega': df_dict['nega'][month_i],
                'neut': df_dict['neut'][month_i],
            }
            ls_=collections.Counter(df_tmp_dict[posneg]['target'].to_list())
            if chi_with_neutral:
                if follow_hisa_impl:
                    ls_not=collections.Counter(
                        list(collections.Counter(df_tmp_dict[negpos]['target'].to_list()))
                       +list(collections.Counter(df_tmp_dict['neut']['target'].to_list()))
                    )
                else:                  
                    ls_not=collections.Counter(
                        df_tmp_dict[negpos]['target'].to_list()
                       +df_tmp_dict['neut']['target'].to_list()
                    )
            else:
                if follow_hisa_impl:
                    ls_not=collections.Counter(
                        list(collections.Counter(df_tmp_dict[negpos]['target'].to_list()))
                    )
                else:                  
                    ls_not=collections.Counter(
                        df_tmp_dict[negpos]['target'].to_list()
                    )
            result = chi2_all(ls_,ls_not)
            results[posneg].append(result)


    record = (
        chi_with_neutral,
        follow_hisa_impl,
        results
    )
    records.append(record)

result_df = pd.DataFrame(records, columns=['chi_with_neutral', 'follow_hisa_impl', 'chi_results_overtime'])

result_df.to_pickle(args.output_chi_result_overtime_pickle)