import io
import os
import numpy as np
from scipy import spatial
from nltk import ngrams
import networkx as nx
import sys
from multiprocessing import Pool
# from sklearn.datasets import fetch_20newsgroups

overall_recall=0
overall_recall_r = 0
all_cps=0
extracted_cps=0

common_phrase_dict={}
dist=[]
L_dict = {}
count = 0

catch_phrases = []

def load_vectors(fname):
	fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
	n, d = map(int, fin.readline().split())
	data = {}
	for line in fin:
		tokens = line.rstrip().split(' ')
		data[tokens[0]] = map(float, tokens[1:])
	return data


# newsgroups_train = fetch_20newsgroups(subset='train')
# newsgroups_test = fetch_20newsgroups(subset='test')
def rank_weights(dirNo):
	legal_data = ''
	with open('combined_text_full.txt', 'r') as f:
		legal_data = f.read()
	f.close()

	newsgroups = []

	for dire in os.listdir('./20_newsgroups'):
		for file in os.listdir(os.path.join('./20_newsgroups', dire)):
			with open(os.path.join(os.path.join('./20_newsgroups', dire), file), 'r', encoding="ISO-8859-1") as f2:
				text = f2.read()
				newsgroups.append(text)
			f2.close()


	documents = []
	for file in os.listdir('./Combined_'+str(dirNo)):
		with open(os.path.join('./Combined_'+str(dirNo), file), 'r',encoding='ISO-8859-1') as f2:
			text = f2.read()
			documents.append(text)
		f2.close()

	for file in os.listdir('./Combined_'+str(dirNo)):
		# document = ''
		# with open(os.path.join('./Combined_modified',file), 'r') as f2:
		# 	text = f2.read()
		# 	text = text.replace('.',' ')
		# 	text = text.lower()
		# 	document = text
		# f2.close()
		with open(os.path.join('./Candidate_'+str(dirNo),file), 'r', encoding='ISO-8859-1') as f2:
			text = f2.read()
			text = text.replace('{','')
			text = text.replace('}','')
			text = text.replace('\'','')
			text = text.lower()
			candidate = text.split(',')
		f2.close()
		candidate = list(set(candidate))
		candidate_weights = []
		for c  in candidate:
			# nl_imp = newsgroups_train.data.count(c)
			# nl_imp+= newsgroups_test.data.count(c)
			# l_imp = legal_data.count(c)
			# candidate_weights.append(l_imp/(nl_imp+1))
			# print(c, (l_imp/(nl_imp+1)))
			nl_imp = 0
			l_imp = 0
			c_nl = 0
			d_nl = 0
			c_l = 0
			d_l = 0
			for news in newsgroups:
				temp = news.count(c)
				if temp>0:
					c_nl +=temp
					d_nl+=1
			for doc in documents:
				temp = doc.count(c)
				if temp>0:
					c_l += temp
					d_l += 1
			nl_imp = c_nl/(d_nl+1)
			l_imp = c_l/(d_l+1)
			candidate_weights.append(l_imp/(nl_imp+1))
			# print(c)
		with open(os.path.join('Phrase_weights', file), 'w') as f2:
			for c in candidate_weights[:-1]:
				f2.write(str(c))
				f2.write(',')
			f2.write(str(candidate_weights[-1]))
		f2.close()
		print("File written")

if __name__=='__main__':
	# data = load_vectors("new_vectors.vec")
	pool = Pool(processes=10)
	pool.map(rank_weights, range(10))
	#with Pool(10) as p:
	#	p.map(rank_weights, [0,1,2,3,4,5,6,7,8,9])




