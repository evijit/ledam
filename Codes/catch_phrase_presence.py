import os
import numpy as np
from spacy.en import English
nlp=English()

import stop_words
stop_words=stop_words.get_stop_words('en')
# stopwords=stopwords.words('english')

stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']
stop_words.extend(stop_words_2)
stop_words.extend(['with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'of', 'to', 'in', 'for', 'on', 'by', 'about', 'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', 'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down', 'off', 'above', 'near', 'and', 'or', 'but', 'nor', 'so', 'for', 'yet', 'after', 'although', 'as', 'as', 'if', 'long', 'because', 'before', 'even', 'if', 'even though', 'once', 'since', 'so', 'that', 'though', 'till', 'unless', 'until', 'what', 'when', 'whenever', 'wherever', 'whether', 'while', 'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'yours', 'his', 'her', 'its', 'ours', 'their', 'few', 'many', 'little', 'much', 'many', 'lot', 'most', 'some', 'any', 'enough', 'all', 'both', 'half', 'either', 'neither', 'each', 'every', 'other', 'another', 'such', 'what', 'rather', 'quite'])
stop_words=list(set(stop_words))
# stopword_file=open("../DATA/Process_resources/stopword.txt",'r')
# stop_words.extend([line.rstrip() for line in stopword_file])


data_dir='/home/ritam/Desktop/LeDAM/DATA/Task_1'

train_cp_dir=data_dir+'/'+'Train_catches'
train_docs_dir=data_dir+'/'+'Train_docs'




common_phrase_dict={}
dist=[]

for i in range(0,100):
	doc_file='case_'+str(i)+'_statement.txt'
	cp_file='case_'+str(i)+'_catchwords.txt'

	doc_file=open(train_docs_dir+'/'+doc_file,errors='ignore')
	cp_file=open(train_cp_dir+'/'+cp_file,errors='ignore')


	for line in cp_file:
		phrase_list=line.strip().lower().split(',')

	phrase_list=[i.strip() for i in phrase_list]	

	L=len(phrase_list)

	text=''
	for line in doc_file:
		text=text+line+' '

	doc=nlp(text)	

	noun_phrases=set()

	for np in doc.noun_chunks:
		np_text=np.text.lower()
		kp=''
		for w in nlp(np_text):
			if w.text_ not in stop_words and w.pos_ !='DET' and w.tag_ !='PRP$'
				kp+=w.text_

		noun_phrases.add(kp.strip())
	
	for word in doc:
		if word.pos_ =='NOUN' or word.pos_=='PROPN':
			noun_phrases.add(word.text.lower())

	print(phrase_list)
	print()		
	print(noun_phrases)
	
	left= len(set(phrase_list)- noun_phrases)/ len(set(phrase_list))
	print(left)
	exit()

	text=text.lower()	

	c=0

	for phrase in phrase_list:
		if phrase in text:
			c+=1

	common_phrase_dict[i]=((L,c,c/L))		

	dist.append(c/L)


print('Min', min(dist))
print('Max', max(dist))
print('Mean', np.mean(dist))
print('Median', np.median(dist))



		