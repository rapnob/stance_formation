
import re
class UserAttributeCollector():
    def __init__(self, use_hisa_findjob_pattern=True):
        self.json_path="/data/str01_03/twitter/hisamits/data/youtube/2020-04_grep/"
        self.job_patterns="/home/hisamits/youtube/youtube_covid/patterns/job_patterns"
        self.age_patterns="/home/hisamits/youtube/youtube_covid/patterns/age_patterns"
        self.gender_patterns="/home/hisamits/youtube/youtube_covid/patterns/gender_patterns"
        self.area_patterns="/home/hisamits/youtube/youtube_covid/patterns/area_patterns"
        self.political_patterns="/home/hisamits/youtube/youtube_covid/patterns/political_patterns"
        self.status_patterns="/home/hisamits/youtube/youtube_covid/patterns/status_pattarns"
        self.use_hisa_findjob_pattern = use_hisa_findjob_pattern
        self.preprocess()
    def match_job(self,profile):
        pat2suffix = []

        for line in open (self.job_patterns):
            if line[0] == '#':
                continue
            suffix, pattern = line[:-1].split (' ')
            if self.use_hisa_findjob_pattern:
                pat2suffix.append ([re.compile (u'(' + pattern + u')(?:。| です|をしています|してます|やってます)*'),suffix])
            else:
                pat2suffix.append ([re.compile (u'(' + pattern + u')(?:。| です|をしています|してます|やってます)'),suffix])
        
        match_result=[]
        for pat in pat2suffix:
            m = pat[0].search (profile)
            if m:
                match_result.append(pat[1])
        return match_result
    
    def find_match(self,profile):
        match_results=[]
        if type(profile)==str:           
            for pat2suffix in self.pat2suffixs:
                match_result='-'
                for pat,suffix in pat2suffix:
                    m = pat.search (profile)
                    if m:
                        match_result=suffix
                match_results.append(match_result)
        else:
            match_results=['-','-','-','-','-']
        return match_results
    def preprocess(self):
        self.pat2suffixs=[]
        categories=['age','gender','job','status','politics']
        for category in categories:
            if category=='age':
                filepath=self.age_patterns
            elif category=='gender':
                filepath=self.gender_patterns
            elif category=='job':
                filepath=self.job_patterns
            #elif category=='area':
                #filepath=self.gender_patterns
            elif category=='status':
                filepath=self.status_patterns
            elif category=='politics':
                filepath=self.political_patterns
            pat2suffix = []
            for line in open (filepath):
                if line[0] == '#':
                    continue
                suffix, pattern = line[:-1].split (' ')
                if self.use_hisa_findjob_pattern:
                    pat2suffix.append ([re.compile (u'(' + pattern + u')(?:。| です|をしています|してます|やってます)*'),suffix])
                else:
                    pat2suffix.append ([re.compile (u'(' + pattern + u')(?:。| です|をしています|してます|やってます)'),suffix])
                    
            self.pat2suffixs.append(pat2suffix)
