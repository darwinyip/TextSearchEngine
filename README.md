# TextSearchEngine
TextSearchEngine is a text search engine.

## How it works
TextSearchEngine indexes every word found from the text files provided. It keeps track of the sentences and filenames of where the words are located, as well as the total word count.

## Requirements
Python 2.7

## Usage
Print top 10 most frequently occuring words in files:

`python doc_indexer.py -i 0.txt 1.txt 2.txt 3.txt 4.txt -t 10`

Find the word "river" in index:

`python doc_indexer.py -i 0.txt 1.txt 2.txt 3.txt 4.txt -f river`
