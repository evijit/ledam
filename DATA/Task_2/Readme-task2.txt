This dataset corresponds to the task Precedence Retrieval (Task 2).
The dataset contains the following two directories:
	1. Current_Cases 
	2. Prior_Cases (A set of older case documents)

And a file named "irled-qrel.txt" that contains the gold standard citation for all current/query cases.

The task is to find relevant prior cases for each of the query documents.

The first folder ("Current_Cases") contains a set of 200 current/query case documents for which the prior cases are to be retrieved.

The second folder ("Prior_Cases") contains a set of 2000 prior cases.  These are to be ranked according to their relevance with each of the query documents in the first folder.

The actual citations in the text of the current/query documents have been removed and replaced with a marker as below:

[?CITATION?]

The [?CITATION?] markers are given to provide the actual positions of the citations. Please note that a query/current document might cite a single prior case more than once. That means, if a document cites N prior cases , it might have more than N markers.
 
