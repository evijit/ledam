This contains the code to clean the documents, then select noun phrases and named entites as the candidates
Then make the vectors for the selected candidates
Finally rank the candidates and choose the top 10 and top 100

The cleaning code is get_catch_key2.py
The vector making code is ranking.py
The selectCandidate.py code runs the code on a set of 40 documents, need to change the number in line 224 and uses networkx, networkx is very slow
The selectCandidate2.py code runs 10 multiprocessing and runs all 400 documents silumtlaneously, and it uses igraph which is faster
The selectionCandidate3.py code runs on 40 documents at a time and uses igraph.
