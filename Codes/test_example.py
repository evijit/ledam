from lexnlp.extract.en import money, citations, conditions, constraints, copyright, courts, definitions, regulations, trademarks, dates, amounts

from lexnlp.nlp.en import tokens

import re
import nltk
import pandas as pd
import numpy as np
import time
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
stanford_dir = st._stanford_jar.rpartition('/')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ':'.join(stanford_jars)

dates1="[0-9][0-9][\/\.-][0-9][0-9][\/\.-][0-9][0-9]+"
only_letters=re.compile('[^a-zA-Z]')

text='''
Kurian Joseph, J.

1. Leave granted in Special Leave Petition (Civil) No. 12495 of 2015

2. Around 46.93 acres of Land was acquired by the Respondent-State of Haryana initiating the proceedings by Notification dated 19.09.1983 issued Under Section 4 of the Land Acquisition Act, 1894. The purpose of acquisition is residential and commercial for Panchkula, Sector-21. The acquired property is in Village Fatehpur. In respect of the same development, we have seen that this Court in many cases has based the fixation of the land value based on acquisition proceedings initiated in 1981 in Village Judian. Those properties in village Judian had access to State Highway and the value fixed by this Court is Rs. 250/- per square yard. In respect of properties situated in the adjoining village of the Appellants namely, Devi Nagar, we have fixed land value at the rate of Rs. 250/- per square yard that was the acquisition initiated in the year 1987 and that property had extensive national highway frontage.

3. Learned Counsel for the Appellants submitted that in all the adjoining villages for the properties acquired for the same purpose, this Court having fixed the land value at Rs. 250/- per square yard and above, the Appellants may also be granted the same value.

4. Shri Sanjay Kumar Tyagi, learned Additional Advocate General for the Respondent-State of Haryana however points out that even according to the Appellants, their claim was only Rs. 125/- per square yard and in any case the land of the Appellants does not have the same advantage when compared to other properties for which this Court had fixed the land value at Rs. 250/- per square yard and above.

5. Learned Counsel appearing for the Appellants however points out that in the matter of fixation of just and fair compensation, the Court is not bound by claim made by the owner. It is for the Court, in the facts and circumstances of each case, to award just and fair compensation.

6. Prior to amendment Act 68 of 1984, the amount of compensation that could be awarded by the Court was limited to the amount claimed by the applicant. Section 25 read as under-

Section 25. Rules as to amount of compensation-

(1) When the applicant has made a claim to compensation, pursuant to any notice given Under Section 9, the amount awarded to him by the court shall not exceed the amount so claimed or be less than the amount awarded by the Collector Under Section 11.

(2) When the applicant has refused to make such claim or has omitted without sufficient reason (to be allowed by the Judge) to make such claim, the amount awarded by the court shall in no case exceed the amount awarded by the Collector.

(3) When the applicant has omitted for a sufficient reason (to be allowed by the Judge) to make such claim, the amount awarded to him by the court shall not be less than, and may exceed, the amount awarded by the Collector.

The amended Section 25 reads as under:

Section 25. Amount of compensation awarded by Court not to be lower than the amount awarded by the Collector- The amount of compensation awarded by the Court shall not be less than the amount awarded by the Collector Under Section 11.

The amendment has come into effect on 24.09.1984.

7. The pre-amended provision put a cap on the maximum; the compensation by court should not be beyond the amount claimed. The amendment in 1984, on the contrary, put a cap on the minimum; compensation cannot be less that what was awarded by the Land Acquisition Collector. The cap on maximum having been expressly omitted, and the cap that is put is only on minimum, it is clear that the amount of compensation that a court can award is no longer restricted to the amount claimed by the applicant. It is the duty of the Court to award just and fair compensation taking into consideration the true market value and other relevant factors, irrespective of the claim made by the owner.

8. Although in the context of the Motor Vehicles Act, 1988, this Court in Sanjay Batham v. Munna Lal Parihar MANU/SC/1280/2011MANU/SC/1280/2011 : (2010) 11 SCC 665 held that-

17. It is true that in the petition filed by him Under Section 166 of the Act, the Appellant had claimed compensation of Rs. 4,20,000/- only, but as held in Nagappa v. Gurudayal Singh MANU/SC/1107/2002MANU/SC/1107/2002 : (2003) 2 SCC 274, in the absence of any bar in the Act, the Tribunal and for that reason any competent Court is entitled to award higher compensation to the victim of an accident.

9. In Bhag Singh and Ors. v. Union Territory of Chandigarh MANU/SC/0265/1985MANU/SC/0265/1985 : (1985) 3 SCC 737, this Court held that there may be situations where the amount higher than claimed may be awarded to the claimant. The Court observed-

3. ... It must be remembered that this was not a dispute between two private citizens where it would be quite just and legitimate to confine the claimant to the claim made by him and not to award him any higher amount than that claimed though even in such a case there may be situations where an amount higher than that claimed can be awarded to the claimant as for instance where an amount is claimed as due at the foot of an account. Here was a claim made by the Appellants against the State Government for compensation for acquisition of their land and under the law, the State was bound to pay to the Appellants compensation on the basis of the market value of the land acquired and if according to the judgments of the learned single Judge and the Division Bench, the market value of the land acquired was higher than that awarded by the Land Acquisition Collector or the Additional District Judge, there is no reason why the Appellants should have been denied the benefit of payment of the market value so determined. To deny this benefit to the Appellants would tantamount to permitting the State Government to acquire the land of the Appellants on payment of less than the true market value. There may be cases where, as for instance, under' agrarian reform legislation, the holder of land may, legitimately, as a matter of social justice with a view to eliminating concentration of land in the hands of a few and bringing about its equitable distribution, be deprived of land which is not being personally cultivated by him or which is in excess of the ceiling area with payment of little compensation or no compensation at all, but where land is acquired under the Land Acquisition Act, 1894, it would not be fair and just to deprive the holder of his land without payment of the true market value when the law, in so many terms, declares that he shall be paid such market value....

10. In Krishi Utpadan Mandi Samiti v. Kanhaiya Lal MANU/SC/0625/2000MANU/SC/0625/2000 : (2000) 7 SCC 756, this Court held that under the amended provisions of Section 25 of the Act, the Court can grant a higher compensation than claimed by the applicant in his pleadings-

17. Award being in this case between the dates 30th April, 1982 and 24th September, 1984 and as per the Union of India and Anr. v. Raghubir Singh (Dead) by L.Rs. etc. (Supra), the amended provisions would be applicable under which there is no restriction that award could only be upto the amount claimed by the claimant. Hence High Court order granting compensation more than what is claimed cannot be said to be illegal or contrary to the provisions of the Act. Hence the review itself, as is confined for the aforesaid reasons, has no merit.

11. Further, in Bhimasha v. Special Land Acquisition Officer and Ors. MANU/SC/8775/2008MANU/SC/8775/2008 : (2008) 10 SCC 797, a three-Judge bench reiterated the principle in Bhag Singh (supra) and rejected the contention that a higher compensation than claimed by the owner in his pleadings cannot be awarded by the Court. In that case, the High Court had concluded that although the market price of the land was Rs. 66,550/- per acre, since the Appellant had only claimed compensation at the rate of Rs. 58,500/- per acre in his pleadings, therefore he could only be awarded compensation limited to his claim. This Court, while reversing the decision of the High Court, awarded the Petitioner the market value, i.e., Rs. 66,550/- per acre thereby holding that the award would not be limited to the claim made by him.

12. In the case of the Appellants herein, it is an admitted position that the properties do not abut the national highway. Admittedly, it is situated about 375 yards away from the national highway and it appears that there is only the narrow Nahan Kothi Road connecting the properties of the Appellants to the national highway. Therefore, it will not be just and proper to award land value of Rs. 250/- per square yard, which is granted to the property in adjoining village. Having regard to the factual and legal position obtained above, we are of the considered view that the just and fair compensation in the case of Appellants would be Rs. 200/- per square yard.

13. Therefore, these appeals are disposed off fixing the land value at Rs. 200/- per square yard and the Appellants shall also be entitled to all the statutory benefits. The amount as above shall be paid and deposited after adjusting the deficit court fee, if any, before the Executing Court within a period of three months from today.


'''

orig_text=str(text)

# Remove dates 

print('Dates')
elems=(list(dates.get_raw_dates(text,return_source=True)))
print(elems)

rep_date_list=[]
for elem in elems:
	date_lim=elem[1]
	if (date_lim[1]-date_lim[0])<=6:
		continue
	rep_text=text[date_lim[0]:date_lim[1]]
	rep_date_list.append(rep_text)	
for i in rep_date_list:
	text=text.replace(i,' <DATE> ')
text= re.sub(dates1,' <DATE> ',text)	
	


start_time=time.time()

rep_money_list=set()
elems=(list(money.get_money(text,return_sources=True)))
print("Money")
print(elems)
for elem in elems:
	rep_money_list.add(elem[-1])	

rep_money_list=list(rep_money_list)

for i in rep_money_list:
	text=text.replace(i,' <MON> ')

print(time.time()-start_time)

# rep_amt_list=[]
# elems=list(amounts.get_amounts(text, return_sources=True))
# print(elems)

# for elem in elems:
# 	amt_lim=elem[1]
# 	rep_text=text[amt_lim[0]:amt_lim[1]]
# 	rep_amt_list.append(rep_text)	

# for i in rep_money_list:
# 	text=text.replace(i,' <AMT> ')



from para_sentence import split_into_sentences
sentences=split_into_sentences(text)
sentence_list=[]

for sentence in sentences:
	if len(only_letters.sub('',sentence))<=4:
		continue
	print(sentence)	
	
	# ner_tags=st.tag(sentence.split())
	# print(ner_tags)
	# for elem in ner_tags:
	# 	if elem[1]=='PERSON':
	# 		sentence=sentence.replace(elem[0],'<PERSON>')		

	sentence_list.append(sentence)

text=""

for elem in sentence_list:
	text=text+elem+'\n'

from textblob import TextBlob

blob= TextBlob(text)
print('Noun Phrases')
print(blob.noun_phrases)

nouns=list(tokens.get_nouns(text))
print('Nouns')
print(nouns)























# print(text)




			
		






'''
print('Money')
elems=(list(money.get_money(text)))
for elem in elems:
	print(elem)
print()
print('Citaions')
elems=(list(citations.get_citations(text)))
for elem in elems:
	print(elem)

print()
print('Conditions')
elems=(list(conditions.get_conditions(text)))
for elem in elems:
	print(elem)

print()
print('Constraints')
elems=(list(constraints.get_constraints(text)))
for elem in elems:
	print(elem)

print()
print('Copyrights')
elems=(list(copyright.get_copyright(text)))
for elem in elems:
	print(elem)

print()
print('Defintions')
elems=(list(definitions.get_definitions(text)))
for elem in elems:
	print(elem)

print()
print('Regulations')
elems=(list(regulations.get_regulations(text)))
for elem in elems:
	print(elem)

print()
print('Trademarks')
elems=(list(trademarks.get_trademarks(text)))
for elem in elems:
	print(elem)


from para_sentence import split_into_sentences

sentences=split_into_sentences(text)

for sentence in sentences:
	print(sentence)
	print()

'''


