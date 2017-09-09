#!/usr/bin/env python

import heapq
import json
import re
from argparse import ArgumentParser, RawTextHelpFormatter
from collections import defaultdict

class SetEncoder(json.JSONEncoder):
    """
    Extends JSONEncoder to encode Sets
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class TextSearchEngine(object):
    """
    TextSearchEngine process text documents, keeps track of words encountered, keeps
    reference of the sentence and the file name where word was found, and the number
    of total occurences for each word.
    """

    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(set))
        self.index_count = defaultdict(int)

    def index_document(self, filename):
        """
        Parse and populates index and index_count

        Args:
            filename: name of file to be parsed
        """
        with open(filename, 'r') as file:
            non_alphanum_pattern = re.compile(r'[^a-zA-Z]')
            for line in file:
                for sentence in filter(None, re.split(r'(?<=\.|\!|\?)[\s]', line.strip())):
                    for word in filter(None, non_alphanum_pattern.split(sentence)):
                        self.index[word.lower()][filename].add(sentence)
                        self.index_count[word.lower()] += 1

    def search(self, word):
        """
        Args:
            word: string to be searched
        Returns:
            {} of file names and set of sentences containing word
        """
        return dict(self.index[word.lower()])

    def top_words(self, n):
        """
        Args:
            n: # of words to return
        Returns:
            {} of top n most frequent words in no particular order
        """
        top_words = heapq.nlargest(n, self.index_count, key=self.index_count.get)
        return {word : self.index[word] for word in top_words}

def to_json(obj):
    """
    Args:
        obj: Object to be JSONified
    Returns:
        Prettified JSON string
    """
    return json.dumps(obj, cls=SetEncoder, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

def main():
    example_text = '''Example:
Print top 10 most frequently occuring words in files:
    python doc_indexer.py -i 0.txt 1.txt 2.txt 3.txt 4.txt -t 10

Find word "river" in index:
    python doc_indexer.py -i 0.txt 1.txt 2.txt 3.txt 4.txt -f river'''

    parser = ArgumentParser(epilog=example_text, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--index', dest='files', nargs='*', help='Indexes words in file')
    parser.add_argument('-f', '--find', dest='word', help='Finds word indexed')
    parser.add_argument('-t', '--top', dest='n', type=int, help='Finds top N words indexed')

    args = vars(parser.parse_args())

    text_seach_engine = TextSearchEngine()

    if args['files'] is not None:
        for filename in args['files']:
            text_seach_engine.index_document(filename)

    if args['word'] is not None:
        print to_json(text_seach_engine.search(args['word']))

    if args['n'] is not None:
        print to_json(text_seach_engine.top_words(args['n']))

if __name__ == '__main__':
    main()
