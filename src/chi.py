from scipy import stats
from tqdm.notebook import tqdm
def chi2(class0,class1,p=0.01,reverse=False, disable_tqdm=True):
    word_list = list(set(set(class0.keys()) | set(class1.keys())))
    N_class0 = sum(class0.values())
    N_class1 = sum(class1.values())

    result=[]
    for word in tqdm(word_list, disable=disable_tqdm):
        data=[[class0[word], N_class0 - class0[word]], [class1[word], N_class1 - class1[word]]]

        bigger_class = 0 if class0[word] > class1[word] else 1
        size=class0[word] if class0[word] > class1[word] else class1[word]

        chi2, p_, dof, ex = stats.chi2_contingency(data, correction=False)
        if reverse==False:
            if p_ < p:
                result.append((bigger_class, word, size))
        else:
            if p_ > p:
                result.append((bigger_class, word, size))
    return result

def chi2_all(class0,class1,reverse=False, disable_tqdm=True):
    word_list = list(set(set(class0.keys()) | set(class1.keys())))
    N_class0 = sum(class0.values())
    N_class1 = sum(class1.values())

    result=[]
    for word in tqdm(word_list, disable=disable_tqdm):
        data=[[class0[word], N_class0 - class0[word]], [class1[word], N_class1 - class1[word]]]

        bigger_class = 0 if class0[word] > class1[word] else 1
        size=class0[word] if class0[word] > class1[word] else class1[word]

        chi2, p_, dof, ex = stats.chi2_contingency(data, correction=False)
        result.append((bigger_class, word, size, p_))
    return result