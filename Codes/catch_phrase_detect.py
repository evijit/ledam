import os
import numpy as np
from textblob import TextBlob

from spacy.en import English
nlp=English()
import inflect
p= inflect.engine()

data_dir='../DATA/Task_1'

train_cp_dir=data_dir+'/'+'Train_catches'
train_docs_dir=data_dir+'/'+'Train_docs'


import stop_words
stop_words=stop_words.get_stop_words('en')
stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']
stop_words.extend(stop_words_2)
stop_words.extend(['with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'of', 'to', 'in', 'for', 'on', 'by', 'about', 'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', 'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off', 'above', 'near', 'and', 'or', 'but', 'nor', 'so', 'for', 'yet', 'after', 'although', 'as', 'as', 'if', 'long', 'because', 'before', 'even', 'if', 'even though', 'once', 'since', 'so', 'that', 'though', 'till', 'unless', 'until', 'what', 'when', 'whenever', 'wherever', 'whether', 'while', 'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'yours', 'his', 'her', 'its', 'ours', 'their', 'few', 'many', 'little', 'much', 'many', 'lot', 'most', 'some', 'any', 'enough', 'all', 'both', 'half', 'either', 'neither', 'each', 'every', 'other', 'another', 'such', 'what', 'rather', 'quite'])
stop_words=list(set(stop_words))

common_phrase_dict={}
dist=[]
L_dict={}


import nltk
# grammar = ('''
#     NP: {<DET>?<ADJ>*<NOUN>+} # NP
#     PNP: {<NP><ADP><NP>} #PP
#     K:{<NP>|<ADJ>}
#     PNP: {<K><ADP><PNP>+} #PP
    
#     ''')

grammar = ('''
    NP: {<DET>?<ADJ>*<NOUN>+} # NP
    PREP:{<ADP>|<PRT>} # prep
    PNP: {<NP><PREP><NP>} #PP
    ANP: {<ADJ><PREP><NP>}# ANP
    K:{<NP>|<ADJ>}
    PNP2: {<K><PREP><PNP>+} #PP
    VB:{<VERB>|<ADV>}
    VNP:{<VB><NP>} # VNP
    
    ''')

grammar2=('''
    NP: {<DET>?<ADJ>*<NOUN>+} # NP
    PREP:{<ADP>|<PRT>} # prep
    VB:{<VERB>|<ADV>}    
    VNP:{<VB><NP>} # VNP
    K:{<NP>|<ADJ>}
    PNP:{<K><PREP><NP>} #ANP
    
''')



chunkParser = nltk.RegexpParser(grammar)
chunkParser2 = nltk.RegexpParser(grammar2)

def leaves(tree,elems):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label() in elems):
        yield subtree.leaves()

def get_terms(tree,elems):
    for leaf in leaves(tree,elems):
        yield [w for w,t in leaf]

def refine_noun_phrase(np_text):
    ref_np=[]
    try:
        dummy_np_text= str(np_text)
        words= nlp(dummy_np_text)

        if words[0].pos_=='DET' or words[0].tag_=='PRP$':
            dummy_np_text= ' '.join([words[i].text for i in range(1,len(words))])
        
        
        ref_np.append(dummy_np_text)
        words=nlp(dummy_np_text)
        
        if len(words)==0:
            return ref_np

        if words[0].pos_=='ADJ' and len(words)>=2:
            dummy_np_text= ' '.join([words[i].text for i in range(1,len(words))])
            ref_np.append(dummy_np_text)

        singulars=[]
        for elem in ref_np:
            if p.singular_noun(elem)!=False:
                singulars.append(p.singular_noun(elem))

        ref_np.extend(singulars)
    except Exception as e:
        print('Exception e')
        print(np_text, dummy_np_text)
    
    return ref_np

overall_recall=0
all_cps=0

for i in range(0,100):
    doc_file='case_'+str(i)+'_statement.txt'
    cp_file='case_'+str(i)+'_catchwords.txt'
    doc_file=open(train_docs_dir+'/'+doc_file,errors='ignore')
    cp_file=open(train_cp_dir+'/'+cp_file,errors='ignore')


    for line in cp_file:
        phrase_list=line.strip().lower().split(',')
    phrase_list=[i.strip() for i in phrase_list]
    L=len(phrase_list)
    all_cps+=L
    
    if L not in L_dict:
        L_dict[L]=0
    L_dict[L]+=1
    
    text=''
    for line in doc_file:
        text=text+line+' '

    doc=nlp(text)
    noun_phrases=[]

    for np in doc.noun_chunks:
        np_text=np.text.lower()
        noun_phrases.append(np_text)

    for word in doc:
        if word.pos_ =='NOUN' or word.pos_=='PROPN' or word.pos_=='ADJ':
            noun_phrases.append(word.text.lower())
    
    
    tagged = nltk.pos_tag(nltk.word_tokenize(text.lower()),tagset='universal')    
    tree = chunkParser.parse(tagged)
    tree2 = chunkParser2.parse(tagged)
    
    terms=get_terms(tree,['NP','PNP','PNP2','VNP','ANP','NOUN'])
    terms2=get_terms(tree2,['NOUN','PNP','NP','VNP'])
    
    for term in terms:
        w=''
        for word in term:
            w+=word+' '
            
        noun_phrases.append(w.strip())
    
    for term in terms2:
        w=''
        for word in term:
            w+=word+' '
            
        noun_phrases.append(w.strip())
    
    
    a=[]
    for np in noun_phrases:
        a.extend(refine_noun_phrase(np.lower()))
    
    noun_phrases=list(a)

    
    
    left= len(set(phrase_list)- set(noun_phrases))
    overall_recall+= L- left
    
    print(L,'\t',left/L)
       
#     if left/L > 0.3 and L>10:
#         print(left)
#         print(cp_file)
#         print(phrase_list)
#         print()
#         print((set(phrase_list)- set(noun_phrases))     
        
#         print()
#         print(set(noun_phrases))
#         print('\n')
    
    text=text.lower()
    c=0
    for phrase in phrase_list:
        if phrase in text:
            c+=1

    common_phrase_dict[i]=((L,c,c/L))
    dist.append(c/L)

print(L_dict)

import numpy as np
print('Min', min(dist))
print('Max', max(dist))
print('Mean', np.mean(dist))
print('Median', np.median(dist))
print('Overall recall', overall_recall/all_cps)