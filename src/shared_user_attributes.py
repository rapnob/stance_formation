

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_chi_results_df_pickle', type=str)
    parser.add_argument('output_attributes_df_pickle', type=str)
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

from tqdm import tqdm

# プロフ欄→職業 のテーブル
from vis_helper import uid2job, uid2desc
from UserAttributeCollector import UserAttributeCollector
uac = UserAttributeCollector()

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
                        config['p_thre'] = p_thre
                        config['topk'] = topk
                        config['chi_with_neutral'] = chi_with_neutral
                        config['follow_hisa_impl'] = follow_hisa_impl
                        config['load_prof_from_Tonly'] = load_prof_from_Tonly
                        config['use_manual_joblabel'] = use_manual_joblabel
                        configs.append(config.copy())
                        config.clear()

config_idx = 0
config = {
    "p_thre": 0.10,
    "topk": 20,

    # posi vs (nega&neutral)にするならTrue, posi vs negaにするならFalse
    "chi_with_neutral": True,

    # ls_not (A vs BのB）の実装を久光準拠にするならTrue
    "follow_hisa_impl": True,
    
    "use_manual_joblabel": False,
    
    "load_prof_from_Tonly": True,
}

# chi_result_df = pd.read_pickle('data/hisa/interim/chi_results_df.pickle')
chi_result_df = pd.read_pickle(args.input_chi_results_df_pickle)

records = []
for config_idx, config in tqdm(enumerate(configs), total=len(configs)):
    # configに該当するchi_resultを読み込んでテーブルを照合する．それだけ
    
    p_thre = config['p_thre']
    topk = config['topk']
    chi_with_neutral = config['chi_with_neutral']
    follow_hisa_impl = config['follow_hisa_impl']
    use_manual_joblabel = config['use_manual_joblabel']
    load_prof_from_Tonly = config['load_prof_from_Tonly']
    
    chi_results_posi = chi_result_df.query(f'chi_with_neutral == {config["chi_with_neutral"]} and follow_hisa_impl == {config["follow_hisa_impl"]}').chi_result_posi.values[0]

    chi_results_nega = chi_result_df.query(f'chi_with_neutral == {config["chi_with_neutral"]} and follow_hisa_impl == {config["follow_hisa_impl"]}').chi_result_nega.values[0]

    words_dict={}
    for bigger_class, uid, num, p_value in chi_results_posi:
        if bigger_class==0 and p_value < p_thre:
            words_dict[uid]=num
    ls_posi_cnt=collections.Counter(words_dict)

    words_dict={}
    for bigger_class, uid, num, p_value in chi_results_nega:
        if bigger_class==0 and p_value < p_thre:
            words_dict[uid]=num

    ls_nega_cnt=collections.Counter(words_dict)

    ls_posi=list(ls_posi_cnt.most_common(topk))
    ls_nega=list(ls_nega_cnt.most_common(topk))

    link_shares = {'n2p': ls_posi, 'n2a': ls_nega}

    # uid2job = often_shared_user_jobinfo.set_index('uid').to_dict('index')

    attributes = {
        'n2p': [],
        'n2a': [],
    }

    for k in ['n2p', 'n2a']:
        for i, l in enumerate(link_shares[k]):
            # desc = uid2desc[uid]
            uid = l[0]
            if load_prof_from_Tonly:
                # descs = df_all[df_all['uid']==l[0]]['user/description'] 
                descs = uid2desc_fromT[uid2desc_fromT['uid']==l[0]]['user/description'] 
                if descs.shape[0] > 0:
                    desc = descs.to_list()[0]
                else:
                    desc = ""
            else:
                desc = uid2desc.get(uid, '')
            if type(desc) == str and len(desc) > 0:
                jobs = uac.find_match(desc)
            else:
                # RTだけする人（ツイート無い人）
                jobs = uac.find_match('')
                # no_desc_usr_num += 1

            if use_manual_joblabel and uid in uid2job and jobs[2] == '-':
                job1, job2 = uid2job[uid]
                jobs[2] = job1 if job2 == '' else job2
            attributes[k].append(jobs)
    record = (p_thre, topk, chi_with_neutral, follow_hisa_impl, use_manual_joblabel, load_prof_from_Tonly, attributes)
    records.append(record)

attributes_df = pd.DataFrame(records, columns=['p_thre', 'topk', 'chi_with_neutral', 'follow_hisa_impl', 'use_manual_joblabel', "load_prof_from_Tonly", 'attributes'])

attributes_df.to_pickle(args.output_attributes_df_pickle)