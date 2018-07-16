import os
import numpy as np

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

	L=len(phrase_list)

	text=''
	for line in doc_file:
		text=text+line+' '

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



		