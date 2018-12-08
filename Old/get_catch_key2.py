import phrasemachine
import os
import io
from nltk.corpus import wordnet as wn
from nltk import pos_tag
import nltk
from nltk.corpus import stopwords
import spacy
import sys
import re
import io
import inflect
q = inflect.engine()

stopWords = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')
skip_ents = ['MONEY', 'QUANTITY', 'DATE', 'TIME', 'PERCENT', 'ORDINAL', 'CARDINAL', 'PERSON']

p = re.compile('([a-z]+\/[0-9]+)')
# p2 = re.compile('^[')

def refine_candidates(candidate):
    candidate2 = []
    # print(candidate)
    for c in candidate:
        # TrainResultsy:
        tempCands = []
        temp_c = c
        # temp_c = c.replace('$','').strip()

        # temp_c = c.strip()
        if len(c)<3:
            continue

        words = nlp(c)
        try:
            if words[0].pos_=='DET' or words[0].tag_=='PRP$':
                temp_c = ' '.join([words[i].text for i in range(1,len(words))])
        except:
            pass
            print("Error")
        tempCands.append(temp_c)
        # print(candidate2)
        # words = nlp(temp_c)
        # try:
        #     if words[0].pos_=='ADJ' and len(words)>=2:
        #         temp_c = ' '.join([words[i].text for i in range(1,len(words))])
        #         candidate2.append(temp_c)
        # except:
        #     print("Error 2")
        singulars=[]
        for elem in tempCands:
            try:
                # print(elem)
                if q.singular_noun(elem)!=False:
                    singulars.append(q.singular_noun(elem))
            except:
                pass
        #print("Done ", c)
        if len(singulars)>0:
            tempCands.extend(singulars)
        # except Exception as e:
        #     print(e)
        candidate2.extend(tempCands)
    # print(candidate2)
    return candidate2


for file in os.listdir('./Combined'):
    error_files = []
    extracted_phrases = []
    with io.open(os.path.join('./Combined',file), 'r', encoding="ISO-8859-1") as f:
        # try:
        text = f.read()
        # print(file)
        # if(os.path.exists('./OldCandidate/'+file)):
              # continue
        # text = text.lower()
        text = text.replace('\n','')
        excep = p.findall(text)
        for w in excep:
            text = text.replace(w, '')
        text = text.replace('  ', ' ')
        sent = text.split('.')

        newtext = ''
        for s in sent:
            doc = nlp(s)
            # if doc[0].pos_=="DET" or doc[0].pos_=="PRP$":
            #     doc = doc[1:]
            # print(doc)
            count = 0
            for token in doc:
                if token.pos_=='NUM':
                    continue
                # elif (token.is_stop):
                #     continue
                elif (token.pos_=="PUNCT" and token.text!='-'):
                    continue
                else:
                    if token.text is '-':
                        newtext+=token.text
                    else:
                        newtext+=token.text+" "
            # if doc[len(doc)-1].pos_ == 'NUM':
            #     newtext = newtext+'.'
            # elif doc[len(doc)-1].is_stop:
            #     newtext+="."
            # elif doc[len(doc)-1].pos_=="PUNCT" and doc[len(doc)-1].text!='-':
            #     newtext+="."
            # else:
            #     newtext+=doc[len(doc)-1].text
            #     newtext+="."
            # print(newtext)
            # sys.exit()
            newtext=newtext.strip()
            newtext+="."

            for e in doc.ents:
                if e.label_=='PERSON':
                    newtext = newtext.replace(e.text,'$$$')
                elif e.label_ == 'DATE':
                    newtext = newtext.replace(e.text,'$$$$')
                elif e.label_ in skip_ents:
                    newtext = newtext.replace(e.text,'')
        newtext = newtext.replace('  ', ' ')
        newtext = newtext.replace('..', '.')
        newtext = newtext.lower()
        # newtext = newtext.rstrip(' ')
        with open(os.path.join('./OldMethod',file), 'w') as f2:
            f2.write(newtext)
        f2.close()
        newsent = newtext.split(".")
        candidate = []
        for s in newsent:
            doc = nlp(s)
            for token in doc.noun_chunks:
                candidate.append(token.text)
            for ent in doc.ents:
                candidate.append(ent.text)

        candidate = list(set(candidate))

        new_candidate=[]
        for elem in candidate:
            new_candidate.append(re.sub('[^a-z- ]+', '', elem).strip())

        candidate=set(list(new_candidate))
            
        candidate = set(refine_candidates(candidate))
        with open(os.path.join('./OldCandidate',file), 'w') as f2:
            f2.write(str(candidate))
        f2.close()
        print(file, "No error")

            # print(candidate)


            # catch_phrases = phrasemachine.get_phrases(text)
            # with open(os.path.join('./TrainResults', file), 'w') as f2:
            #     for phrase in catch_phrases['counts']:
            #         phrase = nltk.word_tokenize(phrase)
            #         phrase = pos_tag(phrase)
            #         sent = str()
            #         for s in phrase:
            #             if(s[1]!='NNP' and s[0] not in stopWords):
            #                 sent+= s[0]
            #                 sent+=' '
            #             # else:
            #             #     print("")
            #         sent = sent.strip(' ')
            #         # print(sent)
            #         f2.write(str(sent))
            #         f2.write(',')
            #         extracted_phrases.append(sent)
            # f2.close()
        # except Exception as e:
        #     print(e)
        #     print(file)
        #     error_files.append(file)
    f.close()
    # cp_file = open(os.path.join('./Train_catches', file.replace('statement','catchwords')))
    # for line in cp_file:
    #     phrase_list=line.strip().lower().split(',')
    # phrase_list=[i.strip() for i in phrase_list]
    # L=len(phrase_list)
    
    # all_cps+=L
    
    # if L not in L_dict:
    #     L_dict[L]=0
    # L_dict[L]+=1
    # phrase_l= set(phrase_list)
    # extracted_ph = set(extracted_phrases)
    # left = 0
    # for p in phrase_l:
    #     flag = 0
    #     for ep in extracted_ph:
    #         if p in ep:
    #             flag = 1
    #     if flag==0:
    #         left+=1
    # # left= len(set(phrase_list)- set(extracted_phrases))
    # overall_recall+= L- left
    # print("Overall: ", overall_recall)
    # extracted_cps+= len(extracted_phrases)
    # # print(extracted_phrases) 
    # # print(phrase_list)
    # print(L,'\t',left/L)
    
    # text=text.lower()
    # c=0
    # for phrase in phrase_list:
    #     if phrase in text:
    #         c+=1

    # common_phrase_dict[count]=((L,c,c/L))
    # count+=1
    # dist.append(c/L)

# print(L_dict)
# print('Overall recall', overall_recall/all_cps)
# print('Overall precision', overall_recall/extracted_cps)

# print(error_files)
# print(len(error_files))
