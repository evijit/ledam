# -*- coding: utf-8 -*-
# Author Ritam Dutt
# Given an input file it splits it into sentences.

import re
import sys
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|www|M|B|Gen|dr|mr|mrs|Hon|Prof|prof|Rev|rev|Rs|rs|No|no)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever|[A-Z])"
abbreviations="([A-Za-z]+[a-z]*[\.]([A-Za-z]+[\.])*[A-Za-z]+)"
#weburls  = "(www)[.]([a-zA-Z0-9]+[.])*(com|net|org|io|gov)"
websites = "[\.](com|net|org|io|gov|edu|in)"
gap="[\s]*"
number = "([0-9]+)"
lastchars=['?','.','!',';']
lower="([a-z])"
default_abbr_list={('a','m'),('c','v'),('e','g'),('e','x'),('i','e'),('p','a'),('p','m'),('p','s')}
bullet_list1='\(([0-9]+)\)'
# bullet_list2='\n([0-9]+[.])'
more_stops='[\.][\s\.]+[\.]'

# ellipses='([\.][\.][\.\s]+)'

# question_ellipses='([?][?\s]+)'
# exclaim_ellipses='([!][!\s]+)'


def split_into_sentences(text):
	# text = re.sub(ellipses,' ',text)
	# text = re.sub(question_ellipses,' ',text)
	# text = re.sub(exclaim_ellipses,' ',text)

	lastchar=text.rstrip()[-1]
	if lastchar not in lastchars:
		text=text+"."
	text = " " + text + "  "
	text = text.replace("\n"," ")
	text = re.sub(bullet_list1,'.',text)
	# text = re.sub(bullet_list2,'.',text)
	text = re.sub(more_stops,'.',text)	
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	text = re.sub(number+"[.]"+number,"\\1<prd>\\2",text)
	#if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
	text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.]"+gap+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + caps + "[.]"," \\1<prd>",text)

	
	abbr_list=re.findall(abbreviations,text)
	

	for i in abbr_list:
		abbr_str=i[0]
		count=abbr_str.count('.')
		if count>=2:
			j=i[0].replace(".","<prd>")
			k=i[0].replace('.','[\.]')
			text=re.sub(k,j,text)
		else:
			las_period_pos=int(abbr_str.rfind("."))
			last_word=abbr_str[las_period_pos+1:]
			first_word=abbr_str[:las_period_pos]
			tup=(first_word.lower(),last_word.lower())
			flag=0


			if  tup in default_abbr_list:
				flag=1   
			if (last_word.islower()==True and last_word!='i') or (len(last_word)==1 and last_word!='I' and last_word!='i'):
				flag=1    

			if flag ==1:    
				j=i[0].replace(".","<prd>")
				k=i[0].replace('.','[\.]')
				text=re.sub(k,j,text)   
				
				# print(text)    
			# if first_word.islower()==True or 
			# print(first_word,last_word)
			# if len(last_word)==1 or last_word not in starters or last_word in lower:
				# k=i[0][:las_period_pos]
				
	if "”" in text: text = text.replace(".”","”.")   
	if "\"" in text: text = text.replace(".\"","\".")   
	if "!" in text: text = text.replace("!\"","\"!")   
	if "?" in text: text = text.replace("?\"","\"?")
	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences if len(s.strip())>0]


	return sentences

import sys
# input_file=sys.argv[1]
# file=open(input_file,'r')
# for line in file:
# 	line=line.rstrip()
# 	sentences=split_into_sentences(line)
# 	print(sentences[1])
# 	print()
		






	
