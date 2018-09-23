import os
import numpy as np
import spacy

nlp=spacy.load('en')

import nltk
from nltk.corpus import stopwords
import gensim
LabeledSentence = gensim.models.doc2vec.LabeledSentence
# nltk.download('stopwords')
# stop_words = stopwords.words('english')


# stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']
# stop_words.extend(stop_words_2)
# stop_words.extend(['with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'of', 'to', 'in', 'for', 'on', 'by', 'about', 'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', 'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off', 'above', 'near', 'and', 'or', 'but', 'nor', 'so', 'for', 'yet', 'after', 'although', 'as', 'as', 'if', 'long', 'because', 'before', 'even', 'if', 'even though', 'once', 'since', 'so', 'that', 'though', 'till', 'unless', 'until', 'what', 'when', 'whenever', 'wherever', 'whether', 'while', 'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'yours', 'his', 'her', 'its', 'ours', 'their', 'few', 'many', 'little', 'much', 'many', 'lot', 'most', 'some', 'any', 'enough', 'all', 'both', 'half', 'either', 'neither', 'each', 'every', 'other', 'another', 'such', 'what', 'rather', 'quite'])
# stop_words=list(set(stop_words))

# stopword_file=open("../DATA/Process_resources/stopword.txt",'r')
# stop_words.extend([line.rstrip() for line in stopword_file])


data_dir='../DATA/Task_1'

train_cp_dir=data_dir+'/'+'Train_catches/'
train_docs_dir=data_dir+'/'+'Train_docs/'


# train_corpus = ""






# for i in range(0,100):
# 	doc_file='case_'+str(i)+'_statement.txt'
# 	# cp_file='case_'+str(i)+'_catchwords.txt'

# 	doc_file=open(train_docs_dir+'/'+doc_file,errors='ignore')
# 	# cp_file=open(train_cp_dir+'/'+cp_file,errors='ignore')
	
	
# 	for line in doc_file:
# 		x = line.strip()
# 		x = x.strip("\n")
# 		x = x.lower()
# 		# print(x)

# 		train_corpus += x
	
# 	train_corpus += "\n"


# with open("train_corpus.txt","w") as f:
# 	f.write(train_corpus)


import gensim
import os
import collections
import smart_open
import random	


def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

train_corpus = list(read_corpus("train_corpus.txt"))
model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=0, epochs=100)
model.build_vocab(train_corpus)

model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

model.save("doc2vec_model")