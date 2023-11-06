"""
    2023/06/26
    Neutral-to-Pro, Anti, Neutralユーザごとシェアされたユーザを収集しカイ2乗検定で各スタンスだけがシェアしやすいユーザを抽出する．
    パラメータが色々あるので全パラメータの結果を保存する．

"""



import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_cp_targets_n2p_before_pickle', type=str)
    parser.add_argument('input_cp_targets_n2a_before_pickle', type=str)
    parser.add_argument('input_cp_targets_n2n_before_pickle', type=str)
    parser.add_argument('output_chi_result_pickle', type=str)
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
logging.info('Loading cp_targets...')

cp_targets_toposi = pd.read_pickle(args.input_cp_targets_n2p_before_pickle)
cp_targets_tonega = pd.read_pickle(args.input_cp_targets_n2a_before_pickle)
cp_targets_toneut = pd.read_pickle(args.input_cp_targets_n2n_before_pickle)
logging.info('Loaded.')

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

records = []
for config_idx, config in tqdm(enumerate(configs), total=len(configs)):
    pass

    chi_with_neutral = config['chi_with_neutral']
    follow_hisa_impl = config['follow_hisa_impl']

    df_tmp_nega=pd.DataFrame(cp_targets_tonega,columns=['target','type'])
    df_tmp_neut=pd.DataFrame(cp_targets_toneut,columns=['target','type'])
    df_tmp_posi=pd.DataFrame(cp_targets_toposi,columns=['target','type'])

    ls_=collections.Counter(df_tmp_posi['target'].to_list())
    if chi_with_neutral:
        if follow_hisa_impl:
            ls_not=collections.Counter(
                list(collections.Counter(df_tmp_nega['target'].to_list()))
               +list(collections.Counter(df_tmp_neut['target'].to_list()))
            )
        else:
            ls_not=collections.Counter(
                df_tmp_nega['target'].to_list()+
                df_tmp_neut['target'].to_list()
            )
    else:
        if follow_hisa_impl:
            ls_not=collections.Counter(
                list(collections.Counter(df_tmp_nega['target'].to_list()))
            )
        else:
            ls_not=collections.Counter(
                df_tmp_nega['target'].to_list()
            )

    result_posi = chi2_all(ls_,ls_not)


    ls_=collections.Counter(df_tmp_nega['target'].to_list())
    if chi_with_neutral:
        if follow_hisa_impl:
            ls_not=collections.Counter(
                list(collections.Counter(df_tmp_posi['target'].to_list()))
               +list(collections.Counter(df_tmp_neut['target'].to_list()))
            )
        else:
            ls_not=collections.Counter(
                df_tmp_posi['target'].to_list()+
                df_tmp_neut['target'].to_list()
            )
    else:
        if follow_hisa_impl:
            ls_not=collections.Counter(
                list(collections.Counter(df_tmp_posi['target'].to_list()))
            )
        else:
            ls_not=collections.Counter(
                df_tmp_posi['target'].to_list()
            )

    result_nega = chi2_all(ls_,ls_not)

    record = (
        chi_with_neutral,
        follow_hisa_impl,
        result_posi,
        result_nega
    )
    records.append(record)    

result_df = pd.DataFrame(records, columns=['chi_with_neutral', 'follow_hisa_impl', 'chi_result_posi', 'chi_result_nega'])

result_df.to_pickle(args.output_chi_result_pickle)