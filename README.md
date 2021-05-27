# Building-Inverted-Positional-Index-and-Answering-Specialized-Wildcard-Entries

Divided the program into 4 tasks

## Task 1
We need documents for building a positional index and we used the seeking alpha website call transcripts as documents. These transcripts can be found [here](https://seekingalpha.com/earnings/earnings-call-transcripts). The task1 uses beautifulsoap to crawl these webpages and save them in a folder.

## Task 2
We build a dictionary consisting of:
1. Date of transcript
2. a dictionary consisting of speaker name and speech.
3. questionnaire dictionary consisting of question and answer.

## Task 3
We remove the stopwords, punctuations, special charecters and do lemmatization and normalization. Then we build the inverted index.

## Task 4
We take the queries from the Queries.txt file and give the output file results.txt. We can give wildcard queries by inserting * symbol in the query.

For runnning the program do the following:
```sh
python task1.py
python task2.py
python task3.py
python task4.py Queries.txt
```
