import pandas as pd
import pickle

df = pd.read_pickle('data/common/uid2desc_fromT.pickle')

uid2desc_06to08 = pickle.load(open('data/common/uid2desc_fromRMQ_06to08.pickle', 'rb'))
uid2desc_09to10 = pickle.load(open('data/common/uid2desc_fromRMQ_09to10.pickle', 'rb'))

uid2desc3 = {uid: attr_dict['user/description'] for uid, attr_dict in df.drop_duplicates(subset='uid').set_index('uid').to_dict('index').items()}

uid2desc = uid2desc3.copy()
uid2desc.update(uid2desc_06to08)
uid2desc.update(uid2desc_09to10)

# プロフ文を見て確認した職業情報
uid2job = dict()
with open('data/table/often_shared_user_job.tsv') as f:
    f.readline()
    lines = f.readlines()
    for line in lines:
        s = line.split('\t')
        if len(line.strip()) == 0:
            continue
        
        if len(s) == 4:
            _, uid_str, _, sname = s
            job1, job2 = '-', '-'
        else:
            # print(s)
            _, uid_str, _, sname, job1, job2, bikou = s
        uid2job[int(uid_str)] = (job1, job2)
        
        
del df, uid2desc_06to08, uid2desc_09to10, uid2desc3

uid2job2_df = pd.read_csv('data/table/often_shared_user_job2.tsv')

uidstr2jobs = uid2job2_df.drop('bikou', axis=1).set_index('uid').to_dict('index')
for uidstr, jobsd in uidstr2jobs.items():
    uid = int(uidstr)
    job1, job2 = jobsd['job'], jobsd['job2']
    if type(job1) != str:
        job1 = '-'
    if type(job2) != str:
        job2 = '-'
    uid2job[uid] = (job1, job2)