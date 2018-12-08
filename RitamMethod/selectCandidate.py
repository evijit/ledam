import io
import os
import numpy as np
from scipy import spatial
from nltk import ngrams
import networkx as nx
import sys
from multiprocessing import Process, Pool
# from gensim.models import FastText

overall_recall=0
overall_recall_r = 0
all_cps=0
extracted_cps=0

# calculations = [0,0,0,0]

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


def select(dirNo):
	global overall_recall, overall_recall_r, all_cps, extracted_cps, common_phrase_dict
	global dist, L_dict, count, catch_phrases
	for file in os.listdir('./Combined_'+str(dirNo)):
		with open(os.path.join('./Combined_'+str(dirNo), file), 'r', encoding='ISO-8859-1') as f:
			text = f.read()
		f.close()
		with open(os.path.join('./Candidate_'+str(dirNo), file), 'r', encoding='ISO-8859-1') as f:
			cand = f.read()
			cand = cand.replace('{','')
			cand = cand.replace('}','')
			cand = cand.replace('\'','')
			cand = cand.lower()
			candidate = cand.split(',')
		f.close()
		candidate = list(set(candidate))
		# print(len(candidate))
		with open(os.path.join('./Phrase_weights', file), 'r') as f:
			weights = f.read()
			wts = weights.split(',')
		f.close()
		for i in range(0, len(wts)):
			wts[i] = float(wts[i])

		candidate_vec = []
		count_error_c = 0
		for c in candidate:
			c_vector = np.zeros((1,100))
			# print(c.rstrip(' ').split(' '))
			for w in c.rstrip(' ').split(' '):
				if w is '' or w is ' ':
					continue
				# print(w, data[w])
				try:
					c_vector= np.add(c_vector, data[w])
				except Exception as e:
					pass
					# print("Candidate",w, file)
					# print(e)
					# sys.exit()
			c_vector = c_vector/(len(c.split(' ')))
			candidate_vec.append(c_vector)

		G=nx.DiGraph()
		for i1, c1 in enumerate(candidate):
			for i2, c2 in enumerate(candidate):
				try:
					pos1 = text.index(c1)
					pos2 = text.index(c2)
				except:
					continue
				if i1!=i2 and (pos1-pos2<=5 or pos2-pos1<=5):
					# print(spatial.distance.cosine(candidate_vec[i1], candidate_vec[i2]))
					wt = spatial.distance.cosine(candidate_vec[i1], candidate_vec[i2])
					if np.isnan(wt):
						wt = 0
					G.add_edge(i1, i2, weight=wt)
					G.add_edge(i2, i1, weight=wt)
		pr = nx.pagerank(G, alpha=0.85, max_iter=500,  tol=1e-02)
		# print(pr)

		final_ranks = []
	# print(len(candidate), len(wts), file)
	# for i1,c1 in enumerate(candidate):
	# 	# print(i1)
	# 	sr = 0
	# 	for i2,c2 in enumerate(candidate):
	# 		if i1==i2:
	# 			continue
	# 		if i1 in G and i2 in G.neighbors(i1):
	# 			cos_score = spatial.distance.cosine(candidate_vec[i1], candidate_vec[i2])
	# 			sr += (1/(1-cos_score))/(G.out_degree(i2))*pr[i2]

	# 	rank_score = 0.15*wts[i1]+sr
	# 	if np.isnan(rank_score):
	# 		rank_score = 0
	# 	final_ranks.append(rank_score)
		for i1, c1 in enumerate(candidate):
			if i1 in pr:
				rank = 0.15*wts[i1]+pr[i1]
			else:
				rank = 0.15*wts[i1]
			if np.isnan(rank):
				rank = 0
			final_ranks.append(rank)

		sort = np.argsort(final_ranks)

		extracted_phrases = []
		extracted_phrases_rec = []
		if len(sort)<100:
			startRec = 0
		else:
			startRec = len(sort)-100
		if len(sort)<10:
			start = 0
		else:
			start = len(sort)-10
		for args in sort[start:]:
			extracted_phrases.append(candidate[args])
		for args in sort[startRec:]:
			extracted_phrases_rec.append(candidate[args])
		with open(os.path.join('./Results', file), 'w') as re:
			re.write(str(extracted_phrases))
			re.write('\n')
			re.write(str(extracted_phrases_rec))
		re.close()

		cp_file = open(os.path.join('./Combined_catches', file.replace('statement','catchwords')))
		for line in cp_file:
			phrase_list=line.strip().lower().split(',')
		phrase_list=[i.strip() for i in phrase_list]
		L=len(phrase_list)

		all_cps+=L
		# calculations[2]+=L
		print(L)
		if L not in L_dict:
			L_dict[L]=0
		L_dict[L]+=1
		phrase_l= set(phrase_list)
		extracted_ph = set(extracted_phrases)
		extracted_ph_rec = set(extracted_phrases_rec)
		left = 0
		for p in phrase_l:
			flag = 0
			for ep in extracted_ph:
				if p in ep:
					flag = 1
			if flag==0:
				left+=1
		left_r = 0
		for p in phrase_l:
			flag = 0
			for ep in extracted_ph_rec:
				if p in ep:
					flag = 1
			if flag==0:
				left_r+=1
		# left= len(set(phrase_list)- set(extracted_phrases))
		overall_recall+= float(L- left)
		# calculations[0]+= float(L- left)
		overall_recall_r+= float(L-left_r)
		# calculations[1] += float(L-left_r)
		extracted_cps+= len(extracted_phrases)
		# calculations[3] += len(extracted_phrases)
		# print(extracted_phrases) 
		print("Overall: ", float(overall_recall)/all_cps, float(overall_recall_r)/all_cps, float(overall_recall)/extracted_cps)
		# print(phrase_list)
		print(L,'\t',float(left_r)/L)
		
		text=text.lower()
		c=0
		for phrase in phrase_list:
			if phrase in text:
				c+=1

		common_phrase_dict[count]=((L,c,float(c)/L))
		count+=1
		dist.append(float(c)/L)

	print(L_dict)
	print('Overall recall', float(overall_recall)/all_cps)
	print('Overall recall 100', float(overall_recall_r)/all_cps)
	print('Overall precision', float(overall_recall)/extracted_cps)
	with open(str(dirNo)+".txt", 'w') as f:
		f.write('Overall Recall ')
		f.write(str(float(overall_recall)/all_cps))
		f.write("\n")
		f.write("Overall recall 100 ")
		f.write(str(float(overall_recall_r)/all_cps))
		f.write("\n")
		f.write("Precision :")
		f.write(str(float(overall_recall)/extracted_cps))
	# return float(overall_recall)/all_cps, float(overall_recall_r)/all_cps, float(overall_recall)/extracted_cps

	

if __name__=='__main__':
	data = load_vectors("Combined.vec")
	# model = FastText.load('new_model.model')
	# calculations = [0,0,0,0]
	recall_10 = []
	recall_100 = []
	prec_10 = []
	# pool = Pool(processes=10)
	# pool.map(select,range(10))
	for i in range(10):
		select(i)
	# for i in range(10):
	# 	p = Process(target=select, args=(i,))
	# 	p.start()
	# 	p.join()
	# for num in range(10):
	# 	p = Process(target=select, args=(num,))
	# 	p.start()
	# 	p.join()
		# select(num)
		# recall_10.append(rec_10)
		# recall_100.append(rec_100)
		# prec_10.append(pre_10)

	# print("Recall on 100 is : ", sum(recall_100)/len(recall_100))
	# print("Precsion on 10 is : ", sum(prec_10)/len(prec_10))


	


