from nltk.parse.stanford import StanfordParser
from para_sentence import split_into_sentences
import nltk

parser=StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

data_dir='/home/ritam/Desktop/LeDAM/DATA/Task_1'

train_docs_dir=data_dir+'/'+'Train_docs'

for i in range(0,100):
	doc_file='case_'+str(i)+'_statement.txt'
	doc_file=open(train_docs_dir+'/'+doc_file,errors='ignore')
	text=''
	for line in doc_file:
		text=text+line+' '

	my_texts=split_into_sentences(text)

	for t in my_texts:
		print(t)


	print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')	
	sents=nltk.sent_tokenize(text)

	for sent in sents:
		print(sent)

	# output_file=open(data_dir+'/PARSED_TEXT/parse_'+str(i)+'.txt','w')

	# for text in texts:
	# 	parse_list=list(parser.raw_parse(text))


	# 	for elem in parse_list:
	# 		print(elem)

	

	
	exit()
		