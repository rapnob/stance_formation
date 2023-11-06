

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_chi_results_df_overtime_pickle', type=str)
    parser.add_argument('output_attributes_df_overtime_pickle', type=str)
    parser.add_argument('--log', default='WARNING', type=str)
    return parser.parse_args()

args = parse_arguments()

import logging
from tqdm import tqdm

fmt = "%(asctime)s %(levelname)s %(name)s : %(message)s"
logging.basicConfig(level=args.log, format=fmt)


import pandas as pd
import collections
import pickle

import sys
sys.path.append('src')
sys.path.append('notebooks')

from vis_helper import uid2job, uid2desc

from UserAttributeCollector import UserAttributeCollector

logging.info('Loading uid2desc...')
uid2desc_fromT = pd.read_pickle('data/common/uid2desc_fromT.pickle')
logging.info('Loaded.')

configs = []
config = dict()
for p_thre in [0.10, 0.05, 0.01]:
    for topk in [20, 30]:
        # posi vs (nega&neutral)にするならTrue, posi vs negaにするならFalse
        for chi_with_neutral in [True, False]:
            # ls_not (A vs BのB）の実装を久光準拠にするならTrue
            for follow_hisa_impl in [True, False]:
                for load_prof_from_Tonly in [False, True]:
                    for use_manual_joblabel in [False, True]:
                        for use_hisa_findjob_pattern in [True, False]:
                            config['use_hisa_findjob_pattern'] = use_hisa_findjob_pattern
                            config['p_thre'] = p_thre
                            config['topk'] = topk
                            config['chi_with_neutral'] = chi_with_neutral
                            config['follow_hisa_impl'] = follow_hisa_impl
                            config['load_prof_from_Tonly'] = load_prof_from_Tonly
                            config['use_manual_joblabel'] = use_manual_joblabel
                            configs.append(config.copy())
                            config.clear()

chi_results_df = pd.read_pickle(args.input_chi_results_df_overtime_pickle)
records = []
for config_idx, config in tqdm(enumerate(configs), total=len(configs), desc='Using all configs...'):

    p_thre = config['p_thre']
    topk = config['topk']
    chi_with_neutral = config['chi_with_neutral']
    follow_hisa_impl = config['follow_hisa_impl']
    use_manual_joblabel = config['use_manual_joblabel']
    load_prof_from_Tonly = config['load_prof_from_Tonly']
    use_hisa_findjob_pattern = config['use_hisa_findjob_pattern']
    
    chi_results_overtime = chi_results_df.query(f'chi_with_neutral == {config["chi_with_neutral"]} and follow_hisa_impl == {config["follow_hisa_impl"]}').chi_results_overtime.values[0]    
    
    attributes = {
        'posi': [],
        'nega': [],
    }
    
    uac = UserAttributeCollector(use_hisa_findjob_pattern=use_hisa_findjob_pattern)
    
    link_share_dict = collections.defaultdict(list)
    for month_i in range(5):
        for posneg in ['posi', 'nega']:
            words_dict={}
            result = chi_results_overtime[posneg][month_i]
            for r in result:
                if r[0]==0:
                    words_dict[r[1]]=r[2]

            ls_cnt=collections.Counter(words_dict)
            ls_=list(ls_cnt.most_common(topk))
            link_share_dict[posneg].append(ls_.copy())

    for k in ['posi', 'nega']:
        link_shares = link_share_dict[k]
        
        for month_i in range(5):
            attribute_n2p = []
            for i, l in enumerate(link_shares[month_i]):
                uid = l[0]
                if load_prof_from_Tonly:
                    # descs = df_all[df_all['uid']==l[0]]['user/description'] 
                    descs = uid2desc_fromT[uid2desc_fromT['uid']==l[0]]['user/description'] 
                    if descs.shape[0] > 0:
                        desc = descs.to_list()[0]
                    else:
                        desc = ""
                else:
                    desc = ''
                    if uid in uid2desc:
                        # ユーザIDからプロフ文を得る
                        desc = uid2desc[uid]
                    jobs = uac.find_match(desc)

                # ユーザIDから職業（人力推定）を得る (人力推定情報があればそっちを優先)
                if use_manual_joblabel and uid in uid2job:
                    # job1はASONAM投稿時ラベルに準拠
                    # job2は新設カテゴリなどを追加
                    job1, job2 = uid2job[uid]
                    if job2 == '' :
                        jobs[2] = job1
                    else:
                        jobs[2] = job2
                attribute_n2p.append((uid, jobs))

            attributes[k].append(attribute_n2p.copy())
            

    record = (p_thre, topk, chi_with_neutral, follow_hisa_impl, use_manual_joblabel, load_prof_from_Tonly, use_hisa_findjob_pattern, attributes)
    records.append(record)
    
    

attributes_df = pd.DataFrame(records, columns=['p_thre', 'topk', 'chi_with_neutral', 'follow_hisa_impl', 'use_manual_joblabel', "load_prof_from_Tonly", 'use_hisa_findjob_pattern', 'attributes_overtime'])

attributes_df.to_pickle(args.output_attributes_df_overtime_pickle)
