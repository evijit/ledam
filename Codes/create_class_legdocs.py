import os
import numpy as np
import re
import nltk
import time
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
stanford_dir = st._stanford_jar.rpartition('/')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ':'.join(stanford_jars)

from lexnlp.extract.en import money, citations, conditions, constraints, copyright, courts, definitions, regulations, trademarks, dates, amounts
from lexnlp.nlp.en import tokens

data_dir='/home/ritam/Desktop/LeDAM/DATA/Task_1'
train_cp_dir=data_dir+'/'+'Train_catches'
train_docs_dir=data_dir+'/'+'Train_docs'


class Legal_Doc:

		def __init__(self,location):
			self.location = location
			self.npl = []
			self.nounns = []

		def getnps(self):
			return self.npl



LD1 = Legal_Doc(location)


